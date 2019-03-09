INSERT INTO cat_colors_info (color, count)
    SELECT color, COUNT(*)
    FROM cats
    GROUP BY color;
