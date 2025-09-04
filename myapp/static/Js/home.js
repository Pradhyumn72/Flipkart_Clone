let inventory = JSON.parse(localStorage.getItem('flipkartInventory')) || [];
        let nextId = parseInt(localStorage.getItem('nextItemId')) || 1;

        function saveToStorage() {
            localStorage.setItem('flipkartInventory', JSON.stringify(inventory));
            localStorage.setItem('nextItemId', nextId.toString());
        }

        function updateStats() {
            document.getElementById('totalItems').textContent = inventory.length;
            
            const totalValue = inventory.reduce((sum, item) => sum + (item.price * item.currentStock), 0);
            document.getElementById('totalValue').textContent = `₹${totalValue.toLocaleString()}`;
            
            const lowStockItems = inventory.filter(item => item.currentStock <= item.maxCapacity * 0.2 && item.currentStock > 0).length;
            document.getElementById('lowStockItems').textContent = lowStockItems;
            
            const outOfStockItems = inventory.filter(item => item.currentStock === 0).length;
            document.getElementById('outOfStockItems').textContent = outOfStockItems;
        }

        function getStockStatus(item) {
            if (item.currentStock === 0) {
                return { class: 'out-of-stock', text: 'Out of Stock' };
            } else if (item.currentStock <= item.maxCapacity * 0.2) {
                return { class: 'low-stock', text: 'Low Stock' };
            } else {
                return { class: 'in-stock', text: 'In Stock' };
            }
        }

        function displayItems(itemsToShow = inventory) {
            const itemsList = document.getElementById('itemsList');
            
            if (itemsToShow.length === 0) {
                itemsList.innerHTML = '<p style="text-align: center; color: #6c757d; font-style: italic; padding: 40px;">No items found. Add some items to get started!</p>';
                return;
            }

            itemsList.innerHTML = itemsToShow.map(item => {
                const stockStatus = getStockStatus(item);
                return `
                    <div class="item-card">
                        <div class="item-header">
                            <span class="item-name">${item.name}</span>
                            <span class="item-price">₹${item.price.toLocaleString()}</span>
                        </div>
                        <div class="item-details">
                            <div><strong>Category:</strong> ${item.category}</div>
                            <div><strong>Stock:</strong> ${item.currentStock}/${item.maxCapacity}</div>
                            <div><span class="stock-status ${stockStatus.class}">${stockStatus.text}</span></div>
                        </div>
                        <div style="margin-bottom: 10px;"><strong>Description:</strong> ${item.description}</div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <small style="color: #6c757d;">Added: ${new Date(item.dateAdded).toLocaleDateString()}</small>
                            <button class="delete-btn" onclick="deleteItem(${item.id})">Delete</button>
                        </div>
                    </div>
                `;
            }).join('');
        }

        function addItem(event) {
            event.preventDefault();
            
            const formData = new FormData(event.target);
            const item = {
                id: nextId++,
                name: formData.get('itemName'),
                price: parseFloat(formData.get('itemPrice')),
                category: formData.get('itemCategory'),
                maxCapacity: parseInt(formData.get('maxCapacity')),
                currentStock: parseInt(formData.get('currentStock')),
                description: formData.get('itemDescription'),
                dateAdded: new Date().toISOString()
            };

            if (item.currentStock > item.maxCapacity) {
                alert('Current stock cannot exceed maximum capacity!');
                return;
            }

            inventory.push(item);
            saveToStorage();
            displayItems();
            updateStats();
            event.target.reset();
            
            // Show success message
            const btn = event.target.querySelector('button');
            const originalText = btn.textContent;
            btn.textContent = 'Item Added! ✓';
            btn.style.background = 'linear-gradient(135deg, #28a745 0%, #20c997 100%)';
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = 'linear-gradient(135deg, #2874f0 0%, #1e88e5 100%)';
            }, 2000);
        }

        function deleteItem(id) {
            if (confirm('Are you sure you want to delete this item?')) {
                inventory = inventory.filter(item => item.id !== id);
                saveToStorage();
                displayItems();
                updateStats();
            }
        }

        function searchItems() {
            const searchTerm = document.getElementById('searchItems').value.toLowerCase();
            const filteredItems = inventory.filter(item => 
                item.name.toLowerCase().includes(searchTerm) ||
                item.category.toLowerCase().includes(searchTerm) ||
                item.description.toLowerCase().includes(searchTerm)
            );
            displayItems(filteredItems);
        }

        function exportData() {
            const dataStr = JSON.stringify(inventory, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'flipkart_inventory.json';
            link.click();
            URL.revokeObjectURL(url);
        }

        function clearLowStock() {
            if (confirm('This will remove all items with low stock. Are you sure?')) {
                inventory = inventory.filter(item => item.currentStock > item.maxCapacity * 0.2);
                saveToStorage();
                displayItems();
                updateStats();
            }
        }

        function bulkDelete() {
            if (confirm('This will delete ALL items from your inventory. This action cannot be undone. Are you sure?')) {
                inventory = [];
                nextId = 1;
                saveToStorage();
                displayItems();
                updateStats();
            }
        }

        // Initialize the dashboard
        document.getElementById('itemForm').addEventListener('submit', addItem);
        displayItems();
        updateStats();

        // Update current stock input max value when max capacity changes
        document.getElementById('maxCapacity').addEventListener('input', function() {
            const currentStockInput = document.getElementById('currentStock');
            currentStockInput.max = this.value;
            if (parseInt(currentStockInput.value) > parseInt(this.value)) {
                currentStockInput.value = this.value;
            }
        });

        // Validate current stock doesn't exceed max capacity
        document.getElementById('currentStock').addEventListener('input', function() {
            const maxCapacity = parseInt(document.getElementById('maxCapacity').value);
            if (parseInt(this.value) > maxCapacity) {
                this.value = maxCapacity;
            }
        });