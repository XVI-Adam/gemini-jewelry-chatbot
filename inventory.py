from taipy.gui import navigate
from taipy.gui import Icon
from taipy import Gui
import prompt
import firestore_db

db=firestore_db.init_firestore()

def create_inventory_table(db,items):
    inventory_table={}
    for i in items:
        # read the inventory collection document specified by item i
        doc = db.collection("inventory").document(i).get()
        # get the field value corresponding to the "count" field
        inv_data = doc.to_dict() or {}
        count = inv_data.get("count", 0)
        # Add these to the inventory table dictionary in the format  
        inventory_table[i] = count

    return inventory_table
         
def create_sales_table(db,items):
    sales_table={"Item":[], "Total Sales":[]}
    for i in items:
        # read the sales collection document specified by i
        doc = db.collection("sales").document(i).get()
        # get the field value corresponding to the "sales" field
        sales_data = doc.to_dict() or {}
        total_sales = sales_data.get("total", 0)
        # Add these to the sales table dictionary in the format shown below:
        sales_table["Item"].append(i)
        sales_table["Total Sales"].append(total_sales)

    return sales_table

inventory_table=create_inventory_table(db,prompt.price.keys())
sales_table=create_sales_table(db,prompt.price.keys())

def button_pressed(state):
    state.inventory_table=create_inventory_table(db,prompt.price.keys())
    state.sales_table=create_sales_table(db,prompt.price.keys())

page="""
<style>
.taipy-table td {
    font-size: 25px 
}

.taipy-table th {
    font-size: 25px 
}
</style>
## Inventory Panel

<|table|data={inventory_table}|width=80%|show_all=True|size=medium|active=False|>

## Total Sales
<|chart|data={sales_table}|type=bar|>

<|Update Display|button|on_action=button_pressed|>
"""

Gui(page=page).run(port="auto", use_reloader=True)
