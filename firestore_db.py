import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import prompt
import random

def init_firestore():
    if not firebase_admin._apps:
        cred = credentials.Certificate("project3-firebase.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

def create_initial_inventory(db):
    coll = db.collection("inventory")
    if hasattr(prompt, 'price') and isinstance(prompt.price, dict):
        for i in prompt.price.keys():
            coll.document(i).set({"count":random.randint(6,20)})
    coll.document("Gold Ring").set({"material": "14K Yellow Gold", "price": 500.00, "stock_quantity": 10, "item_description": "Elegant 14K yellow gold ring", "style": "Classic", "size": 7})
    coll.document("Silver Pendant").set({"material": "Sterling Silver", "price": 75.00, "stock_quantity": 25, "item_description": "Beautiful sterling silver pendant", "style": "Modern"})
    coll.document("Diamond Earrings").set({"stone": "Round Brilliant Cut Diamonds", "price": 1200.00, "stock_quantity": 5, "item_description": "Sparkling diamond earrings", "style": "Elegant"})
    coll.document("Pearl Necklace").set({"material": "Cultured Pearls", "price": 300.00, "stock_quantity": 15, "item_description": "Classic pearl necklace", "style": "Traditional"})
    coll.document("Sapphire Bracelet").set({"stone": "Blue Sapphire", "price": 800.00, "stock_quantity": 8, "item_description": "Stunning blue sapphire bracelet", "style": "Vintage", "size": "7 inches"})
    coll.document("Emerald Brooch").set({"stone": "Emerald", "price": 950.00, "stock_quantity": 3, "item_description": "Exquisite emerald brooch", "style": "Antique"})
    coll.document("Ruby Ring").set({"stone": "Ruby", "price": 1100.00, "stock_quantity": 7, "item_description": "Gorgeous ruby ring", "style": "Classic", "size": 6})
    coll.document("Amethyst Pendant").set({"stone": "Amethyst", "price": 150.00, "stock_quantity": 20, "item_description": "Lovely amethyst pendant", "style": "Bohemian"})
    coll.document("Garnet Earrings").set({"stone": "Garnet", "price": 200.00, "stock_quantity": 12, "item_description": "Charming garnet earrings", "style": "Modern"})
    coll.document("Opal Necklace").set({"stone": "Opal", "price": 400.00, "stock_quantity": 10, "item_description": "Unique opal necklace", "style": "Art Deco"})
    coll.document("Platinum Band").set({"material": "Platinum", "price": 1500.00, "stock_quantity": 6, "item_description": "Sleek platinum band", "style": "Minimalist", "size": 8})
    coll.document("14K Yellow Gold Chain Necklace").set({"material": "14K Yellow Gold", "price": 350.00, "stock_quantity": 15, "item_description": "Classic and versatile 14K yellow gold chain necklace. Perfect for layering or wearing alone.", "style": "Classic", "chain_length": "18 inches"})
    coll.document("18K White Gold Diamond Solitaire Pendant Necklace").set({"material": "18K White Gold", "stone": "Round Brilliant Cut Diamond", "price": 1800.00, "stock_quantity": 7, "item_description": "Elegant 18K white gold necklace featuring a single sparkling diamond solitaire pendant.", "style": "Elegant", "chain_length": "16 inches", "carat_weight": 0.25})
    coll.document("Rose Gold Heart Pendant Necklace").set({"material": "14K Rose Gold", "price": 280.00, "stock_quantity": 20, "item_description": "Sweet and romantic 14K rose gold necklace with a delicate heart pendant.", "style": "Romantic", "chain_length": "17 inches"})
    coll.document("Yellow Gold Figaro Chain Necklace").set({"material": "10K Yellow Gold", "price": 425.00, "stock_quantity": 10, "item_description": "Stylish 10K yellow gold Figaro chain necklace. A bold statement piece.", "style": "Fashion", "chain_length": "20 inches", "chain_width": "3mm"})
    coll.document("White Gold Initial Pendant Necklace").set({"material": "14K White Gold", "price": 315.00, "stock_quantity": 12, "item_description": "Personalized 14K white gold necklace featuring a delicate initial pendant (letter 'A' - example, you'd need to specify the letter).", "style": "Personalized", "chain_length": "18 inches", "initial": "A"})
    coll.document("Yellow Gold Layered Disc Necklace").set({"material": "14K Yellow Gold", "price": 550.00, "stock_quantity": 8, "item_description": "Trendy layered necklace in 14K yellow gold with multiple delicate disc pendants.", "style": "Trendy", "chain_lengths": ["16 inches", "18 inches"]})

def create_initial_sales(db):
     coll = db.collection("sales")
     inventory_docs = db.collection("inventory").stream()
     for doc in inventory_docs:
         item_name = doc.id
         coll.document(item_name).set({"total": random.randint(90, 130)})

if __name__ == "__main__":
    db=init_firestore()
    create_initial_inventory(db)  
    create_initial_sales(db)     

