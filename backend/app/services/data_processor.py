"""
Data Processing Service
Handles validation, cleaning, and processing of uploaded datasets
"""

import asyncio
import json
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union
from io import BytesIO, StringIO
import csv
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)


class DataProcessor:
    """Service for processing and validating uploaded datasets"""

    def __init__(self):
        self.max_file_size = settings.MAX_FILE_SIZE
        self.allowed_file_types = settings.ALLOWED_FILE_TYPES
        self.max_records = settings.MAX_RECORDS_PER_DATASET
        self.strict_validation = settings.DATA_VALIDATION_STRICT

    async def process_upload(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Process uploaded file and return processed data"""
        try:
            # Validate file
            validation_result = await self.validate_file(file_content, filename)
            if not validation_result["valid"]:
                raise ValueError(f"File validation failed: {validation_result['errors']}")

            # Parse file based on type
            file_type = filename.split(".")[-1].lower()

            if file_type == "csv":
                df = await self.parse_csv(file_content)
            elif file_type in ["xlsx", "xls"]:
                df = await self.parse_excel(file_content)
            elif file_type == "json":
                df = await self.parse_json(file_content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

            # Clean and validate data
            cleaned_df = await self.clean_data(df)

            # Generate metadata
            metadata = await self.generate_metadata(cleaned_df, filename)

            # Generate preview
            preview = await self.generate_preview(cleaned_df)

            # Calculate quality score
            quality_score = await self.calculate_quality_score(cleaned_df)

            return {
                "data": cleaned_df.to_dict(orient="records"),
                "metadata": metadata,
                "preview": preview,
                "quality_score": quality_score,
                "processed_at": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Failed to process upload: {e}")
            raise

    async def validate_file(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Validate uploaded file"""
        errors = []
        warnings = []

        # Check file size
        if len(file_content) > self.max_file_size:
            errors.append(f"File size ({len(file_content)} bytes) exceeds maximum ({self.max_file_size} bytes)")

        # Check file type
        file_extension = f".{filename.split('.')[-1].lower()}"
        if file_extension not in self.allowed_file_types:
            errors.append(f"File type {file_extension} not allowed. Allowed types: {self.allowed_file_types}")

        # Check if file is empty
        if len(file_content) == 0:
            errors.append("File is empty")

        # Try to parse file to check format
        try:
            if file_extension == ".csv":
                # Quick CSV validation
                content_str = file_content.decode('utf-8')
                csv.Sniffer().sniff(content_str[:1024])
            elif file_extension in [".xlsx", ".xls"]:
                # Quick Excel validation
                pd.read_excel(BytesIO(file_content), nrows=1)
            elif file_extension == ".json":
                # Quick JSON validation
                json.loads(file_content.decode('utf-8'))
        except Exception as e:
            errors.append(f"File format validation failed: {str(e)}")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    async def parse_csv(self, file_content: bytes) -> pd.DataFrame:
        """Parse CSV file"""
        try:
            content_str = file_content.decode('utf-8')
            df = pd.read_csv(StringIO(content_str))

            if len(df) > self.max_records:
                logger.warning(f"Dataset has {len(df)} records, truncating to {self.max_records}")
                df = df.head(self.max_records)

            return df

        except Exception as e:
            logger.error(f"Failed to parse CSV: {e}")
            raise ValueError(f"Invalid CSV format: {e}")

    async def parse_excel(self, file_content: bytes) -> pd.DataFrame:
        """Parse Excel file"""
        try:
            df = pd.read_excel(BytesIO(file_content))

            if len(df) > self.max_records:
                logger.warning(f"Dataset has {len(df)} records, truncating to {self.max_records}")
                df = df.head(self.max_records)

            return df

        except Exception as e:
            logger.error(f"Failed to parse Excel: {e}")
            raise ValueError(f"Invalid Excel format: {e}")

    async def parse_json(self, file_content: bytes) -> pd.DataFrame:
        """Parse JSON file"""
        try:
            data = json.loads(file_content.decode('utf-8'))

            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                if "data" in data:
                    df = pd.DataFrame(data["data"])
                else:
                    df = pd.DataFrame([data])
            else:
                raise ValueError("JSON must contain array of objects or object with 'data' array")

            if len(df) > self.max_records:
                logger.warning(f"Dataset has {len(df)} records, truncating to {self.max_records}")
                df = df.head(self.max_records)

            return df

        except Exception as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise ValueError(f"Invalid JSON format: {e}")

    async def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize data"""
        try:
            # Make a copy to avoid modifying original
            cleaned_df = df.copy()

            # Remove completely empty rows
            cleaned_df = cleaned_df.dropna(how='all')

            # Remove completely empty columns
            cleaned_df = cleaned_df.dropna(axis=1, how='all')

            # Standardize column names
            cleaned_df.columns = [
                col.strip().lower().replace(' ', '_').replace('-', '_')
                for col in cleaned_df.columns
            ]

            # Handle specific car data cleaning if detected
            if self._is_car_dataset(cleaned_df):
                cleaned_df = await self._clean_car_data(cleaned_df)

            # Convert data types
            cleaned_df = await self._optimize_dtypes(cleaned_df)

            return cleaned_df

        except Exception as e:
            logger.error(f"Failed to clean data: {e}")
            raise

    def _is_car_dataset(self, df: pd.DataFrame) -> bool:
        """Check if dataset appears to be car-related"""
        car_columns = ['brand', 'model', 'year', 'price', 'mileage', 'condition', 'color']
        df_columns = [col.lower() for col in df.columns]

        matches = sum(1 for col in car_columns if any(col in df_col for df_col in df_columns))
        return matches >= 3

    async def _clean_car_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply car-specific data cleaning"""
        try:
            # Standardize price columns
            price_cols = [col for col in df.columns if 'price' in col.lower()]
            for col in price_cols:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')

            # Standardize year columns
            year_cols = [col for col in df.columns if 'year' in col.lower()]
            for col in year_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                # Filter reasonable years (1900-current year + 1)
                current_year = datetime.now().year
                df[col] = df[col].where((df[col] >= 1900) & (df[col] <= current_year + 1))

            # Standardize text fields
            text_cols = [col for col in df.columns if any(keyword in col.lower() for keyword in ['brand', 'model', 'condition', 'color'])]
            for col in text_cols:
                df[col] = df[col].astype(str).str.strip().str.title()

            return df

        except Exception as e:
            logger.error(f"Failed to clean car data: {e}")
            return df

    async def _optimize_dtypes(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize data types for efficiency"""
        try:
            for col in df.columns:
                # Try to convert to numeric if possible
                if df[col].dtype == 'object':
                    # Try numeric conversion
                    numeric_series = pd.to_numeric(df[col], errors='coerce')
                    if not numeric_series.isna().all():
                        # If mostly numeric, convert
                        if numeric_series.notna().sum() / len(df) > 0.8:
                            df[col] = numeric_series
                    else:
                        # Keep as string but optimize
                        df[col] = df[col].astype('string')

            return df

        except Exception as e:
            logger.error(f"Failed to optimize dtypes: {e}")
            return df

    async def generate_metadata(self, df: pd.DataFrame, filename: str) -> Dict[str, Any]:
        """Generate metadata for the dataset"""
        try:
            return {
                "filename": filename,
                "records_count": len(df),
                "columns_count": len(df.columns),
                "columns": [
                    {
                        "name": col,
                        "type": str(df[col].dtype),
                        "null_count": int(df[col].isnull().sum()),
                        "unique_count": int(df[col].nunique())
                    }
                    for col in df.columns
                ],
                "file_size_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
                "data_types": df.dtypes.value_counts().to_dict(),
                "missing_data_percentage": round((df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100, 2)
            }
        except Exception as e:
            logger.error(f"Failed to generate metadata: {e}")
            return {}

    async def generate_preview(self, df: pd.DataFrame, rows: int = 5) -> Dict[str, Any]:
        """Generate preview of the dataset"""
        try:
            return {
                "head": df.head(rows).to_dict(orient="records"),
                "sample": df.sample(min(rows, len(df))).to_dict(orient="records") if len(df) > rows else [],
                "summary_stats": df.describe(include='all').to_dict() if len(df) > 0 else {}
            }
        except Exception as e:
            logger.error(f"Failed to generate preview: {e}")
            return {}

    async def calculate_quality_score(self, df: pd.DataFrame) -> float:
        """Calculate data quality score (0-100)"""
        try:
            if len(df) == 0:
                return 0.0

            score = 100.0

            # Penalize missing data
            missing_percentage = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            score -= missing_percentage * 0.5

            # Penalize duplicate rows
            duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
            score -= duplicate_percentage * 0.3

            # Reward data variety
            avg_unique_ratio = df.nunique().mean() / len(df)
            score += min(avg_unique_ratio * 20, 10)

            # Penalize inconsistent data types in object columns
            for col in df.select_dtypes(include=['object']).columns:
                if df[col].dtype == 'object':
                    # Check for mixed types (numbers as strings, etc.)
                    numeric_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                    if 0 < numeric_count < len(df) * 0.9:
                        score -= 5

            return max(0.0, min(100.0, score))

        except Exception as e:
            logger.error(f"Failed to calculate quality score: {e}")
            return 50.0  # Default score

    async def validate_car_data_schema(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Validate car dataset against expected schema"""
        try:
            required_fields = ['brand', 'model', 'year', 'price']
            optional_fields = ['mileage', 'condition', 'color', 'location', 'fuel_type', 'transmission']

            df_columns = [col.lower() for col in df.columns]

            missing_required = []
            for field in required_fields:
                if not any(field in col for col in df_columns):
                    missing_required.append(field)

            present_optional = []
            for field in optional_fields:
                if any(field in col for col in df_columns):
                    present_optional.append(field)

            return {
                "is_valid_car_dataset": len(missing_required) == 0,
                "missing_required_fields": missing_required,
                "present_optional_fields": present_optional,
                "completeness_score": ((len(required_fields) - len(missing_required)) / len(required_fields)) * 100
            }

        except Exception as e:
            logger.error(f"Failed to validate car data schema: {e}")
            return {"is_valid_car_dataset": False, "error": str(e)}
