CREATE TABLE IF NOT EXISTS [drinks] (
[id] INT NULL,
[title] VARCHAR NULL,
[recipe] VARCHAR NULL
);

INSERT INTO drinks VALUES
(1,'French Cafe au Lait Recipe','[{"name": "1 part hot strong coffee (French roast)", "color": "#44240C", "parts": 1}, {"name": "1 part steamed milk", "color": "#F3F4FC", "parts": 1}]'),
(2,'Pour-Over Coffee','[{"name": "2/3 ounce/18 grams coffee (medium-fine grind)", "color": "#9D6947", "parts": 1}, {"name": "10 ounces/300mL filtered, distilled, or spring water", "color": "#C8EBFC", "parts": 1}]'),
(3,'Cuban Coffee (Cafecito)','[{"name": "1/4 to 1/2 cup coffee (finely ground; or amount needed for pot)", "color": "#85583C", "parts": 1}, {"name": "1 1/2 cups water (or amount for coffee pot)", "color": "#E4F4FB", "parts": 2}, {"name": "1/4 cup white granulated sugar", "color": "#EDE1D9", "parts": 1}]'),
(4,'The Perfect Cappuccino','[{"name": "2 shots (a double shot)", "color": "#BB301B", "parts": 2}, {"name": "4 ounces milk", "color": "#C3CCF4", "parts": 4}]'),
(5,'New Orleans Coffee','[{"name": "4 tablespoons drip-ground coffee", "color": "#C2802F", "parts": 1}, {"name": "2 tablespoons chicory", "color": "#D6E551", "parts": 1}, {"name": "Optional: 1/4 teaspoon salt", "color": "#0B1B3F", "parts": 1}, {"name": "4 cups filtered water", "color": "#A0B8DD", "parts": 1}]'),
(6,'Cold Brew Coffee','[{"name": "1 cup coffee (coarsely ground)", "color": "#593827", "parts": 1}, {"name": "4 cups filtered or distilled water", "color": "#C8EBFC", "parts": 4}]'),
(7,'Affogato','[{"name": "1 scoop vanilla gelato (or ice cream)", "color": "#FCFAF2", "parts": 1}, {"name": "2 ounces hot espresso (or strongly hot brewed coffee)", "color": "#AC0A10", "parts": 1}, {"name": "1 piece chocolate (grated)", "color": "#A88C69", "parts": 1}]'),
(8,'Copycat Maple Pecan Latte','[{"name": "1/4 cup maple syrup", "color": "#F20F28", "parts": 1}, {"name": "1/4 cup pecan butter", "color": "#408BBD", "parts": 1}, {"name": "2 tablespoons brown sugar", "color": "#EDE1D9", "parts": 1}, {"name": "1/2 tablespoon butter", "color": "#BC9B4A", "parts": 1}, {"name": "1/3 cup heavy cream", "color": "#D18C98", "parts": 1}]'),
(9,'White Chocolate Mocha','[{"name": "3/4 cup milk (whole or low-fat)", "color": "#2444B9", "parts": 1}, {"name": "3 tablespoons white chocolate chips", "color": "#A88C69", "parts": 1}, {"name": "1/2 cup prepared coffee", "color": "#593827", "parts": 1}]'),
(10,'Homemade Frappuccino','[{"name": "3 cups coffee (strong; use double the amount of coffee grounds when brewing the coffee)", "color": "#85583C", "parts": 1}, {"name": "2/3 can sweetened condensed milk", "color": "#EF1C3D", "parts": 1}, {"name": "1 cup whole milk", "color": "#F4F4FC", "parts": 1}, {"name": "1/2 vanilla bean", "color": "#FCFAF2", "parts": 1}, {"name": "2 teaspoons vanilla", "color": "#FCF4F7", "parts": 1}]');