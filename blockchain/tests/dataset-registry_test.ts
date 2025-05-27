import { Clarinet, Tx, Chain, Account, types } from 'https://deno.land/x/clarinet@v1.0.0/index.ts';
import { assertEquals } from 'https://deno.land/std@0.90.0/testing/asserts.ts';

Clarinet.test({
    name: "Can register a new dataset",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const deployer = accounts.get('deployer')!;
        const user1 = accounts.get('wallet_1')!;
        
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest123"),
                types.uint(1000000), // 1 STX
                types.utf8('{"title":"Nigerian Car Sales Q1 2024","description":"Comprehensive car sales data","records":2500}')
            ], user1.address)
        ]);
        
        assertEquals(block.receipts.length, 1);
        assertEquals(block.receipts[0].result.expectOk(), types.uint(1));
        
        // Verify dataset was created
        let getDataset = chain.callReadOnlyFn(
            'dataset-registry',
            'get-dataset',
            [types.uint(1)],
            user1.address
        );
        
        const dataset = getDataset.result.expectSome().expectTuple();
        assertEquals(dataset['owner'], user1.address);
        assertEquals(dataset['price'], types.uint(1000000));
        assertEquals(dataset['active'], types.bool(true));
    },
});

Clarinet.test({
    name: "Cannot register dataset with zero price",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const user1 = accounts.get('wallet_1')!;
        
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest123"),
                types.uint(0), // Invalid price
                types.utf8('{"title":"Test Dataset"}')
            ], user1.address)
        ]);
        
        assertEquals(block.receipts.length, 1);
        assertEquals(block.receipts[0].result.expectErr(), types.uint(102)); // ERR_INVALID_PRICE
    },
});

Clarinet.test({
    name: "Can update dataset metadata by owner",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const user1 = accounts.get('wallet_1')!;
        const user2 = accounts.get('wallet_2')!;
        
        // Register dataset
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest123"),
                types.uint(1000000),
                types.utf8('{"title":"Original Title"}')
            ], user1.address)
        ]);
        
        // Update metadata by owner
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'update-dataset-metadata', [
                types.uint(1),
                types.utf8('{"title":"Updated Title","description":"New description"}')
            ], user1.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectOk(), types.bool(true));
        
        // Try to update by non-owner (should fail)
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'update-dataset-metadata', [
                types.uint(1),
                types.utf8('{"title":"Unauthorized Update"}')
            ], user2.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectErr(), types.uint(100)); // ERR_UNAUTHORIZED
    },
});

Clarinet.test({
    name: "Can grant access to dataset",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const deployer = accounts.get('deployer')!;
        const user1 = accounts.get('wallet_1')!;
        const user2 = accounts.get('wallet_2')!;
        
        // Register dataset
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest123"),
                types.uint(1000000),
                types.utf8('{"title":"Test Dataset"}')
            ], user1.address)
        ]);
        
        // Grant access (as contract owner)
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'grant-access', [
                types.uint(1),
                types.principal(user2.address)
            ], deployer.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectOk(), types.bool(true));
        
        // Check access
        let hasAccess = chain.callReadOnlyFn(
            'dataset-registry',
            'has-access',
            [types.uint(1), types.principal(user2.address)],
            user2.address
        );
        
        assertEquals(hasAccess.result, types.bool(true));
    },
});

Clarinet.test({
    name: "Can get user datasets and purchases",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const deployer = accounts.get('deployer')!;
        const user1 = accounts.get('wallet_1')!;
        const user2 = accounts.get('wallet_2')!;
        
        // Register multiple datasets
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest1"),
                types.uint(1000000),
                types.utf8('{"title":"Dataset 1"}')
            ], user1.address),
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest2"),
                types.uint(2000000),
                types.utf8('{"title":"Dataset 2"}')
            ], user1.address)
        ]);
        
        // Grant access to user2 for dataset 1
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'grant-access', [
                types.uint(1),
                types.principal(user2.address)
            ], deployer.address)
        ]);
        
        // Check user1's datasets
        let userDatasets = chain.callReadOnlyFn(
            'dataset-registry',
            'get-user-datasets',
            [types.principal(user1.address)],
            user1.address
        );
        
        const datasets = userDatasets.result.expectTuple()['dataset-ids'].expectList();
        assertEquals(datasets.length, 2);
        
        // Check user2's purchases
        let userPurchases = chain.callReadOnlyFn(
            'dataset-registry',
            'get-user-purchases',
            [types.principal(user2.address)],
            user2.address
        );
        
        const purchases = userPurchases.result.expectTuple()['dataset-ids'].expectList();
        assertEquals(purchases.length, 1);
        assertEquals(purchases[0], types.uint(1));
    },
});

Clarinet.test({
    name: "Can deactivate dataset",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const user1 = accounts.get('wallet_1')!;
        
        // Register dataset
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'register-dataset', [
                types.utf8("ipfs://QmTest123"),
                types.uint(1000000),
                types.utf8('{"title":"Test Dataset"}')
            ], user1.address)
        ]);
        
        // Deactivate dataset
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'deactivate-dataset', [
                types.uint(1)
            ], user1.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectOk(), types.bool(true));
        
        // Verify dataset is inactive
        let getDataset = chain.callReadOnlyFn(
            'dataset-registry',
            'get-dataset',
            [types.uint(1)],
            user1.address
        );
        
        const dataset = getDataset.result.expectSome().expectTuple();
        assertEquals(dataset['active'], types.bool(false));
    },
});

Clarinet.test({
    name: "Platform fee management",
    async fn(chain: Chain, accounts: Map<string, Account>) {
        const deployer = accounts.get('deployer')!;
        const user1 = accounts.get('wallet_1')!;
        
        // Check initial platform fee
        let platformFee = chain.callReadOnlyFn(
            'dataset-registry',
            'get-platform-fee-percentage',
            [],
            deployer.address
        );
        
        assertEquals(platformFee.result, types.uint(5)); // 5% default
        
        // Update platform fee
        let block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'set-platform-fee', [
                types.uint(10) // 10%
            ], deployer.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectOk(), types.bool(true));
        
        // Verify updated fee
        platformFee = chain.callReadOnlyFn(
            'dataset-registry',
            'get-platform-fee-percentage',
            [],
            deployer.address
        );
        
        assertEquals(platformFee.result, types.uint(10));
        
        // Try to set invalid fee (should fail)
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'set-platform-fee', [
                types.uint(25) // > 20% max
            ], deployer.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectErr(), types.uint(102)); // ERR_INVALID_PRICE
        
        // Non-owner cannot set fee
        block = chain.mineBlock([
            Tx.contractCall('dataset-registry', 'set-platform-fee', [
                types.uint(8)
            ], user1.address)
        ]);
        
        assertEquals(block.receipts[0].result.expectErr(), types.uint(100)); // ERR_UNAUTHORIZED
    },
});
