from ..factories import BaseFactory, factory_manager
from ..models import Nation, NationFactory

class TickNation:
    def __init__(self, nation: Nation) -> None:
        self.nation = nation
        pass

    def run_tick(self) -> None:
        self.factory_production()
        self.nation.happiness = min(self.nation.happiness, 10)
        self.nation.happiness = max(self.nation.happiness, -5)
        self.population_consumption()
        self.nation.happiness = min(self.nation.happiness, 10)
        self.nation.happiness = max(self.nation.happiness, -5)
        self.tax_accumulation()
        self.nation.happiness = min(self.nation.happiness, 10)
        self.nation.happiness = max(self.nation.happiness, -5)
        self.population_growth()
        self.nation.happiness = min(self.nation.happiness, 10)
        self.nation.happiness = max(self.nation.happiness, -5)
        self.nation.save()

    def tax_accumulation(self) -> None:
        """
        Calculate how much in taxes a nation has earned, and add it to the nation's taxes_to_collect.
        """
        total_tax = 200 # you'll get at least 200 money in taxes
        if self.nation.happiness > 0:
            population_tax = int(self.nation.population / 200)
            happiness_tax = 50 * (1 + (self.nation.happiness * 0.1))

            total_tax += population_tax + happiness_tax
        
        # Add to pending taxes and save changes
        self.nation.taxes_to_collect += total_tax
        self.nation.save()

    def population_consumption(self) -> None:
        """
        Function for population consuming commodities such as food, power, consumer goods, etc.
        """
        # Food consumption
        food_consumed = int(self.nation.population / 100) # every 100 citizens eat 1 food (they all have anorexia (just like me fr))
        
        if self.nation.system == 2 or self.nation.system == 1: # Capitalist nations and dictatorships eat 5% less food
            food_consumed -= food_consumed * 0.05

        if self.nation.food < food_consumed:
            self.nation.happiness -= 6
            self.nation.food = 0
        else:
            self.nation.food -= food_consumed
            if self.nation.food > (self.nation.population / 100) * 3: # if they can be fed again a few times, preventing famine
                self.nation.happiness += 1

        # Power consumption
        power_consumed = int(self.nation.population / 100) # Every 100 citizens use 1 power
        if self.nation.power < power_consumed:
            self.nation.power = 0
        else:
            self.nation.power -= power_consumed
            self.nation.happiness += 1

        # Money consumption
        if self.nation.system != 2: # dictatorships don't have money upkeep
            base_money_consumed = 250 # base of 250 money for upkeep
            money_consumed_by_population = int(self.nation.population / 1000) # Every 1000 citizens cost you a dolla

            total_money_consumed = base_money_consumed + money_consumed_by_population
            if self.nation.money < total_money_consumed:
                self.nation.money = 0
            else:
                self.nation.money -= total_money_consumed
        
        # Apply all the changes
        self.nation.save()

    def population_growth(self) -> None:
        """
        Calculate population growth and increase the population.
        """
        current_population = self.nation.population
        base_growth = current_population * 0.01
        happiness_growth = base_growth * (self.nation.happiness * 0.05)

        if self.nation.system == 0:
            total_growth = happiness_growth * (1 - 0.05) # capitalist nations grow in population 5% slower
        elif self.nation.system == 1:
            total_growth = happiness_growth * 0.02 # socialist nations grow in population 2% faster
        elif self.nation.system == 2:
            total_growth = happiness_growth * (1 - 0.10) # dictatorships grow in population 10% slower
        
        self.nation.population += int(total_growth)
        self.nation.save()

    def factory_production(self) -> None:
        nation_factories = NationFactory.objects.filter(nation=self.nation).all()

        # Use resources needed to run factories
        for nation_factory in nation_factories:
            factory_type: BaseFactory = factory_manager.get_factory_by_id(nation_factory.factory_type)
            for commodity, quantity in factory_type.input:
                match commodity.value:
                    case "money": 
                        if quantity < self.nation.money: self.nation.money -= quantity
                    case "food": 
                        if quantity < self.nation.food: self.nation.food -= quantity
                    case "power": 
                        if quantity < self.nation.power: self.nation.power -= quantity
                    case "building_materials": 
                        if quantity < self.nation.building_materials: self.nation.building_materials -= quantity
                    case "metal": 
                        if quantity < self.nation.metal: self.nation.metal -= quantity
                    case "consumer_goods": 
                        if quantity < self.nation.consumer_goods: self.nation.consumer_goods -= quantity
            nation_factory.ticks_run += 1
            nation_factory.save()
        self.nation.save()
        