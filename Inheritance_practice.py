
# coding: utf-8

# In[6]:


class Property:
    '''基本 Property 類別'''
    def __init__(self, square_feet='', beds='', baths='', **kwargs):
        super().__init__(**kwargs) #???????
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths
        
    def display(self):
        print("PROPERTY DETAILS")
        print("================")
        print("square footage:  {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()
        
    def prompt_init():
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms:"),
                    baths=input("Enter number of baths")
                    )
        
    prompt_init = staticmethod(prompt_init)
        
    
    '''
    **kwargs : 可被用於多重繼承
    super().__init__ : 預防不是多重繼承鏈中最後一個呼叫
    prompt_init : 立即設為靜態方法
    '''


# In[7]:


def get_valid_input(input_string, valid_options):
    input_string += " ({}) ".format((", ".join(valid_options)))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


# In[8]:


class Apartment(Property):
    '''繼承 Property'''
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")
    
    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry
        
    def display(self):
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s"  % self.laundry)
        print("has balcony: %s" % slef.balcony)
        
        
        
    def prompt_init():
        '''覆寫prompt_init()'''
        parent_init = Property.prompt_init()
        laundry = get_valid_input(
                  "What laundry facilities does the property have?",
                  Apartment.valid_laundries)
        
        balcony = get_valid_input(
                  "Does the property have a balcony?",
                  Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
            })
        return parent_init
    prompt_init = staticmethod(prompt_init)
        
    
       


# In[9]:


class House(Property):
    '''繼承 Property'''
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")
    
    def __init__(self, num_stories='', garage='', fenced='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories
        
    def display(self):
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))
        
        
        
    def prompt_init():
        '''覆寫prompt_init()'''
        parent_init = Property.prompt_init()
        fenced = get_valid_input(
                  "Is the yard fenced?",
                  House.valid_fenced)
        
        garage = get_valid_input(
                  "Is there a garage?",
                  House.valid_garage)
        
        
        num_stories = input("How many stories?")
        
        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
            })
        return parent_init
    prompt_init = staticmethod(prompt_init)


# In[22]:


class Purchase:
    def __init__(self, price='', taxes='', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes
        
    def display():
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))
        
    def prompt_init():
        return dict(
                    price = input("What is the selling prices?"),
                    taxes = input("Waht are the estimated taxes?"))
    
    propt_init = staticmethod(prompt_init)
    


# In[23]:


class Rental:
    def __init__(self, furnished='', utilities='', rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities
        
    def display(self):
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(self.utilities))
        print("furnished:{}".format(self.furnished))
        
    def prompt_init():
        return dict(
                rent = input("What is the monthly rent?"),
                utilities=input("What are the estimated utilities?"),
                furnished = get_valid_input("Is the property furnished?", 
                                           ("yes", "no"))
                    )
    prompt_init = staticmethod(prompt_init)
            
        
        
        
        


# In[24]:


class HouseRental(Rental, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)
    
    

class ApartmentRental(Rental, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Rental.prompt)
        return init
    prompt_init = staticmethod(prompt_init)
    
    
    
class ApartmentPurchase(Purchase, Apartment):
    def prompt_init():
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)
    
    

class HousePurchase(Purchase, House):
    def prompt_init():
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


# In[25]:


class Agent:
    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
        }
    def __init__(self):
        self.property_list = []

    def display_properties(self):
        for property in self.property_list:
            property.display()

    def add_property(self):
        property_type = get_valid_input(
                "What type of property? ",
                ("house", "apartment")).lower()
        payment_type = get_valid_input(
                "What payment type? ",
                ("purchase", "rental")).lower()

        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))
