# TowerDefense
A python Tkinter project for my school computer fair.
![Preview of Tower Defense](/assets/preview.png)

# How to play
You start with a base at (0, 0). You can place cannons and upgrade them with coins to fight minions that come every 100 seconds. Get coins by placing Gold Diggers next to Gold.

# Adding a tower
Create a class that extends Tower
```python
class TestTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y, price)
        self.name = 'name'

    def pre_draw(self, canvas, x, y, size):
        # Instructions to draw BEFORE the rest of the buildings are drawn.
        pass

    def draw(self, canvas, x, y, size):
        super().draw(canvas, x, y, size) # Draws a circle with outline that represents the tower's health (Most towers use this)
        pass

    def post_draw(self, canvas, x, y, size):
        # Instructions to draw AFTER the rest of the buildings are drawn.
        pass

    def update(self, canvas, x, y, size):
        # Updates the game, you can do whatever you want with it (add coins, decrease health, etc)
        pass
```

Now add the name to `Game.towerlist`, and add the Tower to `line 695-698`.
