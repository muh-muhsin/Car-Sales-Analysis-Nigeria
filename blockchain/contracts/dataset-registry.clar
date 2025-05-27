;; Cars360 Dataset Registry Contract
;; Manages dataset registration, metadata, and ownership

;; Constants
(define-constant CONTRACT_OWNER tx-sender)
(define-constant ERR_UNAUTHORIZED (err u100))
(define-constant ERR_DATASET_NOT_FOUND (err u101))
(define-constant ERR_INVALID_PRICE (err u102))
(define-constant ERR_DATASET_EXISTS (err u103))
(define-constant ERR_INVALID_METADATA (err u104))

;; Data Variables
(define-data-var next-dataset-id uint u1)
(define-data-var platform-fee-percentage uint u5) ;; 5% platform fee

;; Data Maps
(define-map datasets
  { dataset-id: uint }
  {
    owner: principal,
    uri: (string-utf8 256),
    price: uint,
    metadata: (string-utf8 512),
    created-at: uint,
    updated-at: uint,
    total-sales: uint,
    rating: uint,
    rating-count: uint,
    active: bool
  }
)

(define-map dataset-access
  { dataset-id: uint, buyer: principal }
  {
    purchased-at: uint,
    access-granted: bool
  }
)

(define-map user-datasets
  { owner: principal }
  { dataset-ids: (list 100 uint) }
)

(define-map user-purchases
  { buyer: principal }
  { dataset-ids: (list 100 uint) }
)

;; Read-only functions

(define-read-only (get-dataset (dataset-id uint))
  (map-get? datasets { dataset-id: dataset-id })
)

(define-read-only (get-dataset-access (dataset-id uint) (buyer principal))
  (map-get? dataset-access { dataset-id: dataset-id, buyer: buyer })
)

(define-read-only (get-user-datasets (owner principal))
  (default-to { dataset-ids: (list) } (map-get? user-datasets { owner: owner }))
)

(define-read-only (get-user-purchases (buyer principal))
  (default-to { dataset-ids: (list) } (map-get? user-purchases { buyer: buyer }))
)

(define-read-only (get-next-dataset-id)
  (var-get next-dataset-id)
)

(define-read-only (get-platform-fee-percentage)
  (var-get platform-fee-percentage)
)

(define-read-only (has-access (dataset-id uint) (buyer principal))
  (match (get-dataset dataset-id)
    dataset-info
      (if (is-eq (get owner dataset-info) buyer)
        true
        (match (get-dataset-access dataset-id buyer)
          access-info (get access-granted access-info)
          false
        )
      )
    false
  )
)

;; Public functions

(define-public (register-dataset 
  (uri (string-utf8 256))
  (price uint)
  (metadata (string-utf8 512))
)
  (let
    (
      (dataset-id (var-get next-dataset-id))
      (current-block-height block-height)
    )
    (asserts! (> price u0) ERR_INVALID_PRICE)
    (asserts! (> (len metadata) u0) ERR_INVALID_METADATA)
    
    ;; Create dataset entry
    (map-set datasets
      { dataset-id: dataset-id }
      {
        owner: tx-sender,
        uri: uri,
        price: price,
        metadata: metadata,
        created-at: current-block-height,
        updated-at: current-block-height,
        total-sales: u0,
        rating: u0,
        rating-count: u0,
        active: true
      }
    )
    
    ;; Update user datasets
    (let
      (
        (current-datasets (get dataset-ids (get-user-datasets tx-sender)))
        (updated-datasets (unwrap! (as-max-len? (append current-datasets dataset-id) u100) ERR_INVALID_METADATA))
      )
      (map-set user-datasets
        { owner: tx-sender }
        { dataset-ids: updated-datasets }
      )
    )
    
    ;; Increment next dataset ID
    (var-set next-dataset-id (+ dataset-id u1))
    
    (ok dataset-id)
  )
)

(define-public (update-dataset-metadata
  (dataset-id uint)
  (new-metadata (string-utf8 512))
)
  (match (get-dataset dataset-id)
    dataset-info
      (begin
        (asserts! (is-eq (get owner dataset-info) tx-sender) ERR_UNAUTHORIZED)
        (asserts! (> (len new-metadata) u0) ERR_INVALID_METADATA)
        
        (map-set datasets
          { dataset-id: dataset-id }
          (merge dataset-info {
            metadata: new-metadata,
            updated-at: block-height
          })
        )
        (ok true)
      )
    ERR_DATASET_NOT_FOUND
  )
)

(define-public (update-dataset-price
  (dataset-id uint)
  (new-price uint)
)
  (match (get-dataset dataset-id)
    dataset-info
      (begin
        (asserts! (is-eq (get owner dataset-info) tx-sender) ERR_UNAUTHORIZED)
        (asserts! (> new-price u0) ERR_INVALID_PRICE)
        
        (map-set datasets
          { dataset-id: dataset-id }
          (merge dataset-info {
            price: new-price,
            updated-at: block-height
          })
        )
        (ok true)
      )
    ERR_DATASET_NOT_FOUND
  )
)

(define-public (deactivate-dataset (dataset-id uint))
  (match (get-dataset dataset-id)
    dataset-info
      (begin
        (asserts! (is-eq (get owner dataset-info) tx-sender) ERR_UNAUTHORIZED)
        
        (map-set datasets
          { dataset-id: dataset-id }
          (merge dataset-info {
            active: false,
            updated-at: block-height
          })
        )
        (ok true)
      )
    ERR_DATASET_NOT_FOUND
  )
)

(define-public (grant-access
  (dataset-id uint)
  (buyer principal)
)
  (match (get-dataset dataset-id)
    dataset-info
      (begin
        ;; Only contract owner or marketplace contract can grant access
        (asserts! (or (is-eq tx-sender CONTRACT_OWNER) 
                     (is-eq contract-caller (as-contract tx-sender))) ERR_UNAUTHORIZED)
        
        ;; Set access
        (map-set dataset-access
          { dataset-id: dataset-id, buyer: buyer }
          {
            purchased-at: block-height,
            access-granted: true
          }
        )
        
        ;; Update user purchases
        (let
          (
            (current-purchases (get dataset-ids (get-user-purchases buyer)))
            (updated-purchases (unwrap! (as-max-len? (append current-purchases dataset-id) u100) ERR_INVALID_METADATA))
          )
          (map-set user-purchases
            { buyer: buyer }
            { dataset-ids: updated-purchases }
          )
        )
        
        ;; Update dataset sales count
        (map-set datasets
          { dataset-id: dataset-id }
          (merge dataset-info {
            total-sales: (+ (get total-sales dataset-info) u1),
            updated-at: block-height
          })
        )
        
        (ok true)
      )
    ERR_DATASET_NOT_FOUND
  )
)

;; Admin functions

(define-public (set-platform-fee (new-fee uint))
  (begin
    (asserts! (is-eq tx-sender CONTRACT_OWNER) ERR_UNAUTHORIZED)
    (asserts! (<= new-fee u20) ERR_INVALID_PRICE) ;; Max 20% fee
    (var-set platform-fee-percentage new-fee)
    (ok true)
  )
)
