import argparse,json,sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path));c.row_factory=sqlite3.Row;c.execute('CREATE TABLE IF NOT EXISTS sales(id INTEGER PRIMARY KEY,product TEXT NOT NULL,quantity INTEGER NOT NULL,unit_price REAL NOT NULL,sold_at TEXT NOT NULL,channel TEXT NOT NULL)');return c
def add(product,quantity,unit_price,sold_at,channel,path=DB):
 quantity=int(quantity);unit_price=float(unit_price)
 if quantity<=0 or unit_price<0:raise ValueError('quantity must be positive and unit price nonnegative')
 with connect(path) as c:cur=c.execute('INSERT INTO sales(product,quantity,unit_price,sold_at,channel) VALUES(?,?,?,?,?)',(product,quantity,unit_price,sold_at,channel));return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM sales ORDER BY sold_at DESC')]
def report(path=DB):
 rows=listing(path);products={};channels={}
 for r in rows:
  revenue=r['quantity']*r['unit_price'];products[r['product']]=products.get(r['product'],0)+revenue;channels[r['channel']]=channels.get(r['channel'],0)+revenue
 return {'sales_records':len(rows),'total_revenue':round(sum(products.values()),2),'revenue_by_product':products,'revenue_by_channel':channels}
def main():
 p=argparse.ArgumentParser(description='Sales insights reporter');s=p.add_subparsers(dest='cmd',required=True);a=s.add_parser('add');a.add_argument('--product',required=True);a.add_argument('--quantity',type=int,required=True);a.add_argument('--unit-price',type=float,required=True);a.add_argument('--sold-at',required=True);a.add_argument('--channel',required=True);s.add_parser('list');s.add_parser('report');x=p.parse_args()
 if x.cmd=='add':print(json.dumps({'id':add(x.product,x.quantity,x.unit_price,x.sold_at,x.channel)}))
 elif x.cmd=='list':print(json.dumps(listing(),indent=2))
 else:print(json.dumps(report(),indent=2))
if __name__=='__main__':main()
