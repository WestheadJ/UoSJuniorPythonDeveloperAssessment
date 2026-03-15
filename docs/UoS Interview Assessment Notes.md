# Assessment Write Up Notes

10/02/26:  
Started outlining the project; with what to use, where to store things, and breaking the problem down  
I am breaking it down so I can tick off all the requirements in scope and helps build a good flow  
Planning the project structure and architecture before you start can allow for an easier, and quicker foot off the ground and can guide the project into a professional and organised layout. Making it easier to program, debug, and explain the project.   
I’m choosing SQLite, due to it being lightweight, quick, and easy to use in python, great for the assessment brief.   
I am creating an ERD to outline the foundation of my database schema and creating a db schema doc that I can reference back to, I would argue that it would be easier to avoid duplicates by having a products dataset, that the orders can link to using the foreign keys, this means orders holds a total order price, and the product holds unit price.   
I am creating an API doc to outline my api, define it, and use it as a reference point.  
I have created the bootstrap with some good ideas. I just think the database could be expanded better, and for a growing dataset, or one that might need updating, this bootstrap is not great or ideal as it is mutated.   
11/02/26:  
While developing, I was thinking of how to stop multiple round trips to the db, instead of getting the customer id and then their orders, I can do a join, but a join makes it so that if there is a customer but no orders, it wouldn’t output anything but with a LEFT JOIN it outputs null if there are no orders, additionally, if the ID doesn’t match the output query would return 0 results  
“SELECT c.customer\_id, c.first\_name, c.last\_name, c.email, c.status as cust\_status, o.order\_id, o.product, o.quantity, o.unit\_price, o.status as order\_status, o.order\_date FROM Customers c LEFT JOIN Orders o ON c.customer\_id \= o.customer\_id WHERE c.customer\_id \= 1”  
12/02/26:  
Making the change to add the order\_total under an auto generated column this way a lot less power on device calculates it, it’s quicker if the SQL engine does it that way. Additionally not sure if they want a summary of all orders, or a total of each, so I will do a total orders csv and an orders summary to showcase 2 different versions.   
13/02/26:  
I knew that whatever I had made with FastAPI would be somewhat wrong due to being new to it, so I have decided to refactor before I submit and do my write up. So i can move into a more suitable and professional project.  
So I researched and found my layout was wrong, I needed to split up my logic and move my schema into a schema folder. I had a confusion in my constant for the CONNECTION and CURSOR for the database, technically the connection opens and closes which is a change, it gets mutated. However the path is a constant. It’s the same with the cursor.