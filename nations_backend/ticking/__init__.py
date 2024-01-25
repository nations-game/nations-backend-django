from ..models import Nation

class Ticking:
    def __init__(self, nation: Nation) -> None:
        self.nation = nation
        pass

    def tax_accumulation(self) -> None:
        total_tax = 200 # you'll get at least 200 money in taxes
        if self.nation.happiness > 0:
            population_tax = int(self.nation.population / 20)
            happiness_tax = 500 * (1 + (self.nation.happiness * 0.1))

            total_tax += population_tax + happiness_tax
        
        # Add to pending taxes and save changes
        self.nation.taxes_to_collect += total_tax
        self.nation.save()

    def population_consumption(self) -> None:
        """
        Function for population consuming commodities such as food, power, consumer goods, etc.
        """
        # Food consumption
        food_consumed = int(self.nation.population / 100) # every 10- citizens eat 1 food (they all have anorexia (just like me fr))
        if self.nation.food < food_consumed:
            self.nation.happiness -= 6
            self.nation.food = 0
        else:
            self.nation.food -= food_consumed
            if self.nation.food > (self.nation.population / 100) * 3: # if they can be fed again a few times, preventing famine
                self.nation.happiness += 1

        # Power consumption
        power_consumed = int(self.nation.population / 5) # Every 20 citizens use 1 power
        if self.nation.power < power_consumed:
            self.nation.power = 0
        else:
            self.nation.power -= power_consumed
            self.nation.happiness += 1

        # Money consumption
        if self.nation.system != 2: # dictatorships don't have money upkeep
            base_money_consumed = 500 # base of 500 money for upkeep
            money_consumed_by_population = int(self.nation.population / 200) # Every 200 citizens cost you a dolla

            total_money_consumed = base_money_consumed + money_consumed_by_population
            if self.nation.money < total_money_consumed:
                self.nation.money = 0
            else:
                self.nation.money -= total_money_consumed
        
        # Apply all the changes
        self.nation.save()

    def happiness_calculation(self) -> None:
        ...

    def population_growth(self) -> None:
        """
        Calculate population growth and increase the population.
        """
        current_population = self.nation.population
        base_growth = current_population * 0.1
        happiness_growth = base_growth * (self.nation.happiness * 0.1)

        if self.nation.system == 0:
            total_growth = happiness_growth * (1 - 0.05) # capitalist nations grow in population 5% slower
        elif self.nation.system == 1:
            total_growth = happiness_growth * 0.02 # socialist nations grow in population 2% faster
        elif self.nation.system == 2:
            total_growth = happiness_growth * (1 - 0.02) # dictatorships grow in population 2% slower
        
        self.nation.population += total_growth
        self.nation.save()