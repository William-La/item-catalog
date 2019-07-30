from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, Base

engine = create_engine('sqlite:///itemCatalog.db')

Base.metadata.bind = engine

session = DBSession()


category1 = Category(name="Action")

session.add(category1)
session.commit()


action1 = Item(category=category1, title="Revengers: Last Game", desc="A diverse group of heroes team up, make up some physics, and go shopping for some fancy jewelry.")

session.add(action1)
session.commit()


action2 = Item(category=category1, title="John 'Keanu Reeves' Wick 3", desc="I actually haven't watched any of the John Wick movies so I am not qualified to write a description for this. But Keanu Reeves is in it so it must be good.")

session.add(action2)
session.commit()


category2 = Category(name="Adventure")

session.add(category2)
session.commit()


advent1 = Item(category=category2, title="The 4th Story Regarding Toys", desc="A group of supposedly inanimate objects go on a road trip to... save a spork?")

session.add(advent1)
session.commit()


advent2 = Item(category=category2, title="The King of Lions", desc="A live action remake of a classic childhood film that doesn't actually feature a live lion in it.")

session.add(advent2)
session.commit()


category3 = Category(name="Animated")

session.add(category3)
session.commit()


animate1 = Item(category=category3, title="Kid from Brooklyn: Introduction to many Araneae", desc="Honestly the best animated movie to this date 10/10 highly recommend also the soundtrack is amazing it's on Netflix what are you waiting for.")

session.add(animate1)
session.commit()


animate2 = Item(category=category3, title="Utopian Zoo", desc="A bunny and a fox try to prevent their friends and family from becoming feral? I really only remember the sloth from that one scene.")

session.add(animate2)
session.commit()


category4 = Category(name="Biography")

session.add(category4)
session.commit()


bio1 = Item(category=category4, title="Unseen Figurines", desc="A story of discrimination, grit, and great achievement that follows black, female mathematicians working for NASA and assisting in America's first obital spaceflight.")

session.add(bio1)
session.commit()


bio2 = Item(category=category4, title="The All-Inclusive Hypothesis", desc="The emergence of world renowned scientist Stevie Eagling, best known for his hypothesis regardign the middle of the universe. ")

session.add(bio2)
session.commit()


category5 = Category(name="Comedy")

session.add(category5)
session.commit()


comedy1 = Item(category=category5, title="Minhaj Hasan: Prom Prince", desc="A stand-up comedy special detailing a first generation American's growth and struggle against harsh realities in the Untied States.")

session.add(comedy1)
session.commit()


comedy2 = Item(category=category5, title="Arachnidboy: No Longer in New York", desc="Boy tries to go on vacation with his friends and classmates, but runs into some trippy illusion stuff that personally gave me one too many scares. He ends up with his crush though so that was cute.")

session.add(comedy2)
session.commit()


#category6 = Category(name="Fantasy")
#category7 = Category(name="Romance")
#category8 = Category(name="Thriller")
#category9 = Category(name="Science Fiction")
