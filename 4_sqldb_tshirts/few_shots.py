few_shots = [
    # --- Existing examples (your 6) ---

    {'Question': "How many t-shirts do we have left for Nike in XS size and white color?",
     'SQLQuery': "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS';",
     'SQLResult': "Result of the SQL query",
     'Answer': "91"},

    {'Question': "How much is the total price of the inventory for all S-size t-shirts?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE size = 'S';",
     'SQLResult': "Result of the SQL query",
     'Answer': "22292"},

    {'Question': "If we have to sell all the Levi’s T-shirts today with discounts applied, how much revenue will our store generate (post discounts)?",
     'SQLQuery': """SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue
                    FROM (
                        SELECT SUM(price * stock_quantity) AS total_amount, t_shirt_id
                        FROM t_shirts
                        WHERE brand = 'Levi'
                        GROUP BY t_shirt_id
                    ) a
                    LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "16725.4"},

    {'Question': "If we have to sell all the Levi’s T-shirts today, how much revenue will our store generate without discount?",
     'SQLQuery': "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi';",
     'SQLResult': "Result of the SQL query",
     'Answer': "17462"},

    {'Question': "How many white color Levi's shirts do I have?",
     'SQLQuery': "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White';",
     'SQLResult': "Result of the SQL query",
     'Answer': "290"},

    {'Question': "How much sales amount will be generated if we sell all large size t-shirts today in Nike brand after discounts?",
     'SQLQuery': """SELECT SUM(a.total_amount * ((100 - COALESCE(discounts.pct_discount, 0)) / 100)) AS total_revenue
                    FROM (
                        SELECT SUM(price * stock_quantity) AS total_amount, t_shirt_id
                        FROM t_shirts
                        WHERE brand = 'Nike' AND size = 'L'
                        GROUP BY t_shirt_id
                    ) a
                    LEFT JOIN discounts ON a.t_shirt_id = discounts.t_shirt_id;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "8199.000000"},

    # --- NEW ADVANCED EXAMPLES ---

    {'Question': "Which brand has the highest total stock across all colors and sizes?",
     'SQLQuery': """SELECT brand, SUM(stock_quantity) AS total_stock
                    FROM t_shirts
                    GROUP BY brand
                    ORDER BY total_stock DESC
                    LIMIT 1;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "Nike"},

    {'Question': "What is the average price of Adidas t-shirts after applying discounts?",
     'SQLQuery': """SELECT AVG(price * ((100 - COALESCE(pct_discount, 0)) / 100)) AS avg_discounted_price
                    FROM t_shirts
                    LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id
                    WHERE brand = 'Adidas';""",
     'SQLResult': "Result of the SQL query",
     'Answer': "28.5"},

    {'Question': "List top 3 most expensive t-shirts (price-wise) available in stock.",
     'SQLQuery': """SELECT brand, color, size, price
                    FROM t_shirts
                    ORDER BY price DESC
                    LIMIT 3;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "[('Van Huesen', 'Black', 'XL', 50), ('Nike', 'Red', 'L', 49), ('Levi', 'Blue', 'M', 48)]"},

    {'Question': "Which color of Nike t-shirts has the highest total inventory value (price * stock)?",
     'SQLQuery': """SELECT color, SUM(price * stock_quantity) AS total_value
                    FROM t_shirts
                    WHERE brand = 'Nike'
                    GROUP BY color
                    ORDER BY total_value DESC
                    LIMIT 1;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "Black"},

    {'Question': "Find the average discount percentage offered across all t-shirts that have a discount.",
     'SQLQuery': "SELECT AVG(pct_discount) FROM discounts;",
     'SQLResult': "Result of the SQL query",
     'Answer': "23.5"},

    {'Question': "How many unique brand-color-size combinations are available?",
     'SQLQuery': "SELECT COUNT(DISTINCT CONCAT(brand, '-', color, '-', size)) FROM t_shirts;",
     'SQLResult': "Result of the SQL query",
     'Answer': "100"},

    {'Question': "Find the top 2 brands contributing the most to total revenue after applying discounts.",
     'SQLQuery': """SELECT t.brand, SUM(t.price * t.stock_quantity * ((100 - COALESCE(d.pct_discount, 0)) / 100)) AS total_revenue
                    FROM t_shirts t
                    LEFT JOIN discounts d ON t.t_shirt_id = d.t_shirt_id
                    GROUP BY t.brand
                    ORDER BY total_revenue DESC
                    LIMIT 2;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "[('Nike', 24000), ('Adidas', 22000)]"},

    {'Question': "Show total stock for each size category, ordered from smallest to largest size.",
     'SQLQuery': """SELECT size, SUM(stock_quantity) AS total_stock
                    FROM t_shirts
                    GROUP BY size
                    ORDER BY FIELD(size, 'XS', 'S', 'M', 'L', 'XL');""",
     'SQLResult': "Result of the SQL query",
     'Answer': "[('XS', 520), ('S', 640), ('M', 680), ('L', 710), ('XL', 590)]"},

    {'Question': "Which t-shirt has the maximum discount percentage and what brand does it belong to?",
     'SQLQuery': """SELECT t.brand, t.color, t.size, d.pct_discount
                    FROM t_shirts t
                    JOIN discounts d ON t.t_shirt_id = d.t_shirt_id
                    ORDER BY d.pct_discount DESC
                    LIMIT 1;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "Adidas, Blue, L, 45.00"},

    {'Question': "Rank all brands based on their average discounted price (lowest to highest).",
     'SQLQuery': """SELECT brand, 
                           AVG(price * ((100 - COALESCE(pct_discount, 0)) / 100)) AS avg_discounted_price,
                           RANK() OVER (ORDER BY AVG(price * ((100 - COALESCE(pct_discount, 0)) / 100))) AS price_rank
                    FROM t_shirts
                    LEFT JOIN discounts ON t_shirts.t_shirt_id = discounts.t_shirt_id
                    GROUP BY brand;""",
     'SQLResult': "Result of the SQL query",
     'Answer': "[('Adidas', 27.1, 1), ('Levi', 28.4, 2), ('Van Huesen', 29.3, 3), ('Nike', 31.5, 4)]"}
]
