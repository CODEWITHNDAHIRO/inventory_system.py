import json
from abc import ABC, abstractmethod
from datetime import datetime
class InventoryItem(ABC):
    """
    Abstract Base Class representing a generic inventory item.
    Demonstrates: ABSTRACTION
    """
    def __init__(self, item_id, name, price, quantity):
        self.item_id = item_id
        self.name = name
        self._price = price  # Protected attribute (Encapsulation)
        self._quantity = quantity

    @property
    def total_value(self):
        """Getter for total value calculation."""
        return self._price * self._quantity

    @abstractmethod
    def get_inventory_report(self):
        """Abstract method to be implemented by subclasses."""
        pass

class PerishableItem(InventoryItem):
    """
    Represents items with an expiry date.
    Demonstrates: INHERITANCE and POLYMORPHISM
    """
    def __init__(self, item_id, name, price, quantity, expiry_date):
        super().__init__(item_id, name, price, quantity)
        self.expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d")

    def get_inventory_report(self):
        """Polymorphic implementation of the report."""
        status = "Fresh" if self.expiry_date > datetime.now() else "EXPIRED"
        return f"[Perishable] {self.name} | Status: {status} | Value: ${self.total_value:,.2f}"
class ElectronicItem(InventoryItem):
    """
    Represents hardware/electronics.
    Demonstrates: INHERITANCE and POLYMORPHISM
    """
    def __init__(self, item_id, name, price, quantity, warranty_months):
        # super() links this to the main InventoryItem class
        super().__init__(item_id, name, price, quantity)
        self.warranty_months = warranty_months

    
    def get_inventory_report(self):
        """Overrides the parent method to show warranty info."""
        return (f"ELECTRONIC: {self.name} (ID: {self.item_id}) | "
                   f"Warranty: {self.warranty_months} months | "
                    f"Stock: {self._quantity}")
    
class Warehouse:
    """
    Manages a collection of inventory items.
    Demonstrates: ENCAPSULATION
    """
    def __init__(self, location):
        self.location = location
        self.__items = []  # Private attribute: items cannot be modified directly

    def add_item(self, item):
        if isinstance(item, InventoryItem):
            self.__items.append(item)
            print(f"Added {item.name} to {self.location} warehouse.")

    def generate_full_report(self):
        print(f"\n--- Inventory Report: {self.location} ---")
        for item in self.__items:
            # Polymorphism in action: calling the same method on different item types
            print(item.get_inventory_report())
    def save_to_file(self, filename="inventory.json"):
        data = []
        for item in self.__items:
            # We convert the object data into a dictionary for JSON
            item_data = {
                "item_id": item.item_id,
                "name": item.name,
                "price": item._price,
                "quantity": item.quantity,
                "type": type(item).__name__
            }
            # If it's perishable, save the expiry date too
            if isinstance(item, PerishableItem):
                item_data["expiry_date"] = item.self.expiry_date.strftime("%Y-%m-%d")
            data.append(item_data)
        
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory saved to {filename}")
    def load_from_file(self, filename="inventory.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                # Clear current items to avoid duplicates on load
                self._Warehouse__items = [] 
                
                for entry in data:
                    if entry["type"] == "PerishableItem":
                        new_item = PerishableItem(
                            entry["item_id"], 
                            entry["name"], 
                            entry["price"], 
                            entry["quantity"], 
                            entry["expiry_date"]
                        )
                    else:
                        # Add logic here if you create other non-perishable types later
                        pass 
                    
                    self.add_item(new_item)
            print(f"Successfully loaded {len(data)} items from {filename}")
        except FileNotFoundError:
            print("Error: No inventory file found to load.")
        except Exception as e:
            print(f"An error occurred while loading: {e}")


    def load_from_file(self, filename="inventory.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                for entry in data:
                    # Logic to recreate objects from the JSON data goes here
                    print(f"Loading {entry['name']}...")
        except FileNotFoundError:
            print("No saved inventory found.")



# --- Execution ---
if __name__ == "__main__":
    # Initialize Warehouse
    kigali_hub = Warehouse("Kigali Free Zone")

    # Create Items
    milk = PerishableItem("M001", "Inyange Milk", 1.2, 500, "2025-12-30")
    old_bread = PerishableItem("B022", "Local Bread", 0.5, 20, "2023-01-01")

    # Add to Inventory
    kigali_hub.add_item(milk)
    kigali_hub.add_item(old_bread)

    # Generate Report
    kigali_hub.generate_full_report()