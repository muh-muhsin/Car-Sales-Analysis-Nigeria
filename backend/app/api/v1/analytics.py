"""
Analytics endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from app.core.database import get_db
from app.core.security import get_optional_user
from app.models.dataset import Dataset, DatasetAccess
from app.models.user import User
from app.models.transaction import Transaction

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/marketplace-stats")
async def get_marketplace_stats(
    db: Session = Depends(get_db),
    current_user: Optional[Dict[str, Any]] = Depends(get_optional_user)
):
    """Get marketplace statistics"""
    try:
        # Basic counts
        total_datasets = db.query(Dataset).filter(Dataset.is_active == True).count()
        total_users = db.query(User).filter(User.is_active == True).count()
        total_transactions = db.query(DatasetAccess).count()
        
        # Revenue statistics
        total_revenue = db.query(func.sum(DatasetAccess.price_paid)).scalar() or 0
        
        # Recent activity (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_datasets = db.query(Dataset).filter(
            Dataset.created_at >= thirty_days_ago,
            Dataset.is_active == True
        ).count()
        
        recent_transactions = db.query(DatasetAccess).filter(
            DatasetAccess.created_at >= thirty_days_ago
        ).count()
        
        # Top datasets by sales
        top_datasets = db.query(
            Dataset.id,
            Dataset.title,
            Dataset.total_sales,
            Dataset.total_revenue
        ).filter(
            Dataset.is_active == True
        ).order_by(desc(Dataset.total_sales)).limit(5).all()
        
        # Top sellers
        top_sellers = db.query(
            User.id,
            User.wallet_address,
            User.username,
            User.display_name,
            User.total_uploads,
            User.total_earnings
        ).filter(
            User.is_active == True,
            User.total_uploads > 0
        ).order_by(desc(User.total_earnings)).limit(5).all()
        
        return {
            "overview": {
                "total_datasets": total_datasets,
                "total_users": total_users,
                "total_transactions": total_transactions,
                "total_revenue": round(total_revenue, 2)
            },
            "recent_activity": {
                "new_datasets_30d": recent_datasets,
                "transactions_30d": recent_transactions
            },
            "top_datasets": [
                {
                    "id": dataset.id,
                    "title": dataset.title,
                    "total_sales": dataset.total_sales,
                    "total_revenue": round(dataset.total_revenue, 2)
                }
                for dataset in top_datasets
            ],
            "top_sellers": [
                {
                    "id": seller.id,
                    "wallet_address": seller.wallet_address,
                    "username": seller.username,
                    "display_name": seller.display_name,
                    "total_uploads": seller.total_uploads,
                    "total_earnings": round(seller.total_earnings, 2)
                }
                for seller in top_sellers
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get marketplace stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve marketplace statistics"
        )


@router.get("/price-trends")
async def get_price_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get price trends over time"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get daily average prices
        daily_prices = db.query(
            func.date(DatasetAccess.created_at).label('date'),
            func.avg(DatasetAccess.price_paid).label('avg_price'),
            func.count(DatasetAccess.id).label('transaction_count')
        ).filter(
            DatasetAccess.created_at >= start_date
        ).group_by(
            func.date(DatasetAccess.created_at)
        ).order_by('date').all()
        
        return {
            "price_trends": [
                {
                    "date": trend.date.isoformat(),
                    "average_price": round(float(trend.avg_price), 2),
                    "transaction_count": trend.transaction_count
                }
                for trend in daily_prices
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get price trends: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve price trends"
        )


@router.get("/category-distribution")
async def get_category_distribution(
    db: Session = Depends(get_db)
):
    """Get distribution of datasets by category/tags"""
    try:
        # Get all datasets with tags
        datasets = db.query(Dataset.tags).filter(
            Dataset.is_active == True,
            Dataset.tags.isnot(None)
        ).all()
        
        # Count tag occurrences
        tag_counts = {}
        for dataset in datasets:
            if dataset.tags:
                for tag in dataset.tags:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Sort by count
        sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "categories": [
                {
                    "name": tag,
                    "count": count,
                    "percentage": round((count / len(datasets)) * 100, 1) if datasets else 0
                }
                for tag, count in sorted_tags[:10]  # Top 10 categories
            ]
        }
        
    except Exception as e:
        logger.error(f"Failed to get category distribution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve category distribution"
        )


@router.get("/quality-metrics")
async def get_quality_metrics(
    db: Session = Depends(get_db)
):
    """Get quality metrics across all datasets"""
    try:
        # Quality score distribution
        quality_ranges = [
            (90, 100, "Excellent"),
            (80, 89, "Good"),
            (70, 79, "Fair"),
            (60, 69, "Poor"),
            (0, 59, "Very Poor")
        ]
        
        quality_distribution = []
        for min_score, max_score, label in quality_ranges:
            count = db.query(Dataset).filter(
                Dataset.is_active == True,
                Dataset.quality_score >= min_score,
                Dataset.quality_score <= max_score
            ).count()
            
            quality_distribution.append({
                "range": f"{min_score}-{max_score}",
                "label": label,
                "count": count
            })
        
        # Average quality score
        avg_quality = db.query(func.avg(Dataset.quality_score)).filter(
            Dataset.is_active == True
        ).scalar() or 0
        
        # Rating distribution
        rating_distribution = []
        for rating in range(1, 6):
            count = db.query(Dataset).filter(
                Dataset.is_active == True,
                Dataset.average_rating >= rating,
                Dataset.average_rating < rating + 1
            ).count()
            
            rating_distribution.append({
                "rating": rating,
                "count": count
            })
        
        return {
            "quality_distribution": quality_distribution,
            "average_quality_score": round(float(avg_quality), 2),
            "rating_distribution": rating_distribution
        }
        
    except Exception as e:
        logger.error(f"Failed to get quality metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve quality metrics"
        )


@router.get("/user-activity")
async def get_user_activity(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get user activity metrics"""
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # New users over time
        daily_signups = db.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('new_users')
        ).filter(
            User.created_at >= start_date,
            User.is_active == True
        ).group_by(
            func.date(User.created_at)
        ).order_by('date').all()
        
        # Active users (users who made transactions)
        active_users = db.query(func.count(func.distinct(DatasetAccess.user_id))).filter(
            DatasetAccess.created_at >= start_date
        ).scalar() or 0
        
        # User engagement metrics
        total_active_users = db.query(User).filter(User.is_active == True).count()
        
        return {
            "daily_signups": [
                {
                    "date": signup.date.isoformat(),
                    "new_users": signup.new_users
                }
                for signup in daily_signups
            ],
            "active_users_period": active_users,
            "total_active_users": total_active_users,
            "engagement_rate": round((active_users / total_active_users) * 100, 2) if total_active_users > 0 else 0
        }
        
    except Exception as e:
        logger.error(f"Failed to get user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user activity"
        )
