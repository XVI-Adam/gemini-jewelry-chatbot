import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from taipy.gui import navigate
from taipy.gui import Icon
from taipy import Gui
import prompt
import time
from proj2_image_gen import gen_order_image
import firestore_db


MODEL_ID="gemini-1.5-flash"
db=firestore_db.init_firestore()

def check_inventory(db,order):
    for i in order:
        item=i['item']
        quantity=i['quantity']
        
        doc=db.collection("inventory").document(item)
        sales_doc= db.collection("sales").document(item)
        
        inv_snapshot = doc.get()
        sales_snapshot = sales_doc.get()
        
        inv_data = inv_snapshot.to_dict() or {}
        sales_data = sales_snapshot.to_dict() or {}
        
        t=sales_data.get("total",0)
        c=inv_data.get("count",0)

        print(item, quantity, t, c)
        
        if quantity > c:
            i['quantity']=c
            i['modified_order']=True
            i['num_items_dropped']=quantity-c
            
            sales_doc.set({"total": t + c}, merge=True)
            doc.set({"count": 0}, merge=True)
            
        else: 
            i['modified_order']=False
            i['num_items_dropped']=0
            
            doc.set({"count": c - quantity}, merge=True)
            sales_doc.set({"total": t + quantity}, merge=True)

    return order



def user_replied(state, var_name, value):
    global chat
    order_table={"Quantity":[],
                 "Item":[],
                 "Unit Price":[],
                 "Amount":[]
                 }

    print("Enter pressed")
    if len(state.user_string)==0:
        print("Empty Response")
    else:
        print("Entered:",state.user_string)
        response =chat.send_message(state.user_string)
        state.user_string=""
        r=json.loads(extract_json(response.text))
        print(r)
        state.bot_string="### "+r["response"]
        if r["status"]=="complete":
            print("order complete")     # will print in the shell – used for debugging
            state.bot_string+="\n### In a few seconds you will be taken to the checkout page"
            modified_order=check_inventory(db,r["cart"]) 
            any_modified = any(item.get('modified_order') for item in modified_order)
            
            if any_modified:
                state.bot_string += "\n### Some items were adjusted due to limited stock."
                
            image_prompt="Generate an image that contains the following items: "

            total=0     # variable to hold the final total cost
            
            dropped_message = ""
            
            for item in r["cart"]:
                item_name = item["item"]
                quantity = item["quantity"]
                unit_price = item["price"]
                amount = quantity * unit_price
                
                order_table["Item"].append(item_name)
                order_table["Quantity"].append(quantity)
                order_table["Unit Price"].append(unit_price)
                order_table["Amount"].append(amount)
                
                total += amount
                image_prompt += f"{quantity} {item_name}, "
                
                if item["modified_order"]:
                    dropped_message += f"\n### Note: {item['num_items_dropped']} units of '{item_name}' were dropped due to low inventory."
            
            image_prompt = image_prompt.strip().rstrip(',')
            
            state.total_string+=str(total)
            
            if dropped_message != "":
                state.total_string += f"\nNote the following order changes: \n {dropped_message}\n"
                
            state.order_table=order_table.copy()
            print(image_prompt)
            
            result=gen_order_image(client, image_prompt)
            if result!=None:
            	state.order_image=result
                                      
            navigate(state,to="Pay")                   # move to the new page – which is named "Pay"


def new_order(state, var_name, value):
    global chat 
    state.bot_string="### Hi there! What can I get for you?"
    state.user_string= ""
    state.total_string= "### Total=$"
    state.order_table = {"Quantity": [],
                         "Item": [],
                         "Unit Price": [],
                         "Amount": []}
    
    chat = client.chats.create(
        model=MODEL_ID,
        config=chat_config,
    )
    state.order_image="thank_you.jpg"
    navigate(state, to="Order")


def extract_json(s):
    return s[8:-5]

load_dotenv() # GEMINI_API_KEY should be defined in a .env file
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

chat_config = types.GenerateContentConfig(
    system_instruction=prompt.system_instruction,
    temperature=2,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain"
)

chat = client.chats.create(
    model=MODEL_ID,
    config=chat_config,
)

bot_string="### Hi there! What can I get for you?"
user_string=""

total_string="### Total=$"

order_table={"Quantity":[],
             "Item":[],
             "Unit Price":[],
             "Amount":[]
             }

icon = Icon("tap_to_pay.png", "Tap To Pay")

IMAGE_URL="https://media.giphy.com/media/pPzjpxJXa0pna/giphy.gif?cid=ecf05e47blg5r2dcw3kbjwbqvjswjf0zfn3pg1zy4op2w7sn&ep=v1_gifs_search&rid=giphy.gif&ct=g"
page1="""
# Oro Latino Jewelry Shop – Best In New York
 
<|{IMAGE_URL}|image|>

<|{bot_string}|mode=markdown|text|>

<|{user_string}|width=400|change_delay=-1|on_action=user_replied|input|>

"""

order_image="thank_you.jpg"

page2="""
<style>
.taipy-table td {
    font-size: 25px 
}

.taipy-table th {
    font-size: 25px 
}
</style>

# Checkout Page

## Your order consists of the following items:
<|table|data={order_table}|id=my_table|width=50%|show_all=True|size=medium|active=False|>

<|{total_string}|mode=markdown|text|>

<|{icon}|button|on_action=new_order|>

<|{order_image}|image|>

"""

page3="""
## Inventory Panel
"""



pages={
	"Order":page1,
	"Pay":page2,
    "Inventory":page3
}


Gui(pages=pages).run(port="auto", use_reloader=True)

