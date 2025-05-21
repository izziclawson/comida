import csv
import pandas as pd
import sys
import random
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init(autoreset=True)

def load_data():
    """Load and clean the recipe data"""
    file_path = "bigSheet.csv"
    try:
        df = pd.read_csv(file_path, quotechar='"', escapechar='\\', on_bad_lines='warn')
        # Clean column names and data
        df.columns = df.columns.str.strip().str.lower()
        df = df.applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
        return df
    except Exception as e:
        print(f"\n{Fore.RED}Error loading your recipe list:{Style.RESET_ALL}", e)
        sys.exit(1)

def show_help():
    """Display help message"""
    print(f"""
    {Fore.CYAN}Hi love!{Style.RESET_ALL} Let's make food feel easier. This script helps you figure out what to eat or prep
    based on your mood — whether you're tired, picky, or just overwhelmed.

    It will ask you how you're feeling:
    - Do you want something {color_tag('hot')} or {color_tag('cold')}?
    - Are you in the mood for {color_tag('sweet')}, {color_tag('salty')}, or a {color_tag('mix of both')}?
    - Do you want something {color_tag('crunchy')}, {color_tag('soft')}, {color_tag('drinkable')}, or something else?
    - Are you in the mood for something {color_tag('light')} or {color_tag('filling')}?
    - Do you have the energy to cook ({color_tag('max')}), a little energy ({color_tag('min')}), or {color_tag('none')} at all?

    Just press Enter if you're not sure — that's totally okay.
    After you answer, you'll see options that match how you feel.
    And you'll also see whether you have the stuff for them or not ❤️
    """)

def color_tag(tag):
    """Return colored version of tags"""
    colors = {
        'hot': Fore.RED,
        'cold': Fore.BLUE,
        'sweet': Fore.MAGENTA,
        'salty': Fore.YELLOW,
        'both': Fore.CYAN,
        'crunchy': Fore.LIGHTYELLOW_EX,
        'soft': Fore.LIGHTMAGENTA_EX,
        'drinkable': Fore.LIGHTBLUE_EX,
        'light': Fore.GREEN,
        'filling': Fore.LIGHTRED_EX,
        'none': Fore.WHITE,
        'min': Fore.YELLOW,
        'max': Fore.RED
    }
    for key, color in colors.items():
        if key in tag.lower():
            return f"{color}{tag}{Style.RESET_ALL}"
    return tag

def get_random_recipes(df, num_recipes):
    """Get random recipe suggestions"""
    if num_recipes > len(df):
        num_recipes = len(df)
    random_recipes = df.sample(n=num_recipes)
    
    print(f"\n{Fore.CYAN}Here are some random ideas to get you started:{Style.RESET_ALL}")
    for _, row in random_recipes.iterrows():
        print_recipe(row)
    print(f"\n{Fore.LIGHTBLUE_EX}Hope these spark some inspiration!{Style.RESET_ALL}")

def get_preferences():
    """Collect user preferences"""
    print(f"\n{Fore.CYAN}Hi sweetpea! Let's figure out what kind of meal fits your mood today.{Style.RESET_ALL}")
    try:
        temp_want = input(f"Do you want something {color_tag('hot')}, {color_tag('cold')}, or you're not sure? ").strip().lower()
        flavor_want = input(f"Feeling {color_tag('sweet')}, {color_tag('salty')}, or {color_tag('both')}? ").strip().lower()
        texture_want = input(f"Do you want something {color_tag('crunchy')}, {color_tag('soft')}, or {color_tag('drinkable')}? ").strip().lower()
        density_want = input(f"Are you in the mood for something {color_tag('light')} or {color_tag('filling')}? ").strip().lower()
        time_want = input(f"How much energy do you have? Type {color_tag('none')}, {color_tag('min')}, or {color_tag('max')}: ").strip().lower()
        return temp_want, flavor_want, texture_want, density_want, time_want
    except Exception as e:
        print(f"{Fore.RED}Something went wrong while collecting your preferences:{Style.RESET_ALL}", e)
        sys.exit(1)

def filter_recipes(df, preferences):
    """Filter recipes based on user preferences"""
    temp_want, flavor_want, texture_want, density_want, time_want = preferences
    filtered = df.copy()
    
    try:
        if temp_want:
            filtered = filtered[filtered["temp"] == temp_want]
        if flavor_want:
            if flavor_want != "both":
                filtered = filtered[filtered["flavor"] == flavor_want]
        if texture_want:
            if texture_want == "soft":
                filtered = filtered[filtered["texture"].isin(["soft", "drinkable"])]
            else:
                filtered = filtered[filtered["texture"] == texture_want]
        if density_want:
            filtered = filtered[filtered["density"] == density_want]
        if time_want:
            if time_want == "min":
                filtered = filtered[filtered["time"].isin(["min", "none"])]
            elif time_want == "max":
                filtered = filtered[filtered["time"].isin(["max", "min", "none"])]
            else:
                filtered = filtered[filtered["time"] == time_want]
        return filtered
    except KeyError as e:
        print(f"{Fore.RED}One of the columns is missing in your CSV:{Style.RESET_ALL}", e)
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}Something went wrong while filtering recipes:{Style.RESET_ALL}", e)
        sys.exit(1)

def print_recipe(row):
    """Print a recipe with colored formatting"""
    stock_status = f"{Fore.GREEN}✅ in stock{Style.RESET_ALL}" if row.get("in stock", "no") == "yes" else f"{Fore.RED}❌ not in stock{Style.RESET_ALL}"
    
    try:
        print(f"- {Fore.LIGHTYELLOW_EX}{row.get('recipe name', 'Unnamed Recipe').title()}{Style.RESET_ALL} ("
              f"flavor: {color_tag(row.get('flavor', '[missing]'))}, "
              f"temp: {color_tag(row.get('temp', '[missing]'))}, "
              f"texture: {color_tag(row.get('texture', '[missing]'))}, "
              f"density: {color_tag(row.get('density', '[missing]'))}, "
              f"time: {color_tag(row.get('time', '[missing]'))}) — {stock_status}")
    except KeyError as e:
        print(f"{Fore.RED}Oops — couldn't show one of the recipe entries because a column is missing:{Style.RESET_ALL}", e)

def main():
    """Main program flow"""
    # Show help if requested
    if len(sys.argv) > 1 and sys.argv[1].lower() == "help!":
        show_help()
    
    df = load_data()
    
    while True:
        # Initial choice
        print(f"\n{Fore.CYAN}What would you like to do?{Style.RESET_ALL}")
        print(f"1. {Fore.LIGHTGREEN_EX}Get personalized recommendations based on my mood{Style.RESET_ALL}")
        print(f"2. {Fore.LIGHTBLUE_EX}Get random recipe ideas to inspire me{Style.RESET_ALL}")
        print(f"3. {Fore.LIGHTRED_EX}Exit{Style.RESET_ALL}")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            preferences = get_preferences()
            filtered = filter_recipes(df, preferences)
            
            if filtered.empty:
                print(f"\n{Fore.MAGENTA}Sorry love, nothing matches all your inputs right now.{Style.RESET_ALL}")
                print(f"{Fore.LIGHTBLUE_EX}Would you like to try seeing results that take a little more energy or have a different flavor?{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}Here are some tasty ideas based on your vibe today:{Style.RESET_ALL}")
                for _, row in filtered.iterrows():
                    print_recipe(row)
        
        elif choice == "2":
            try:
                num_recipes = int(input(f"\n{Fore.CYAN}How many random recipes would you like to see? (1-{len(df)}): {Style.RESET_ALL}"))
                get_random_recipes(df, num_recipes)
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")
                continue
        
        elif choice == "3":
            print(f"\n{Fore.LIGHTMAGENTA_EX}Goodbye sweetpea! Hope you found something delicious to enjoy. ❤️{Style.RESET_ALL}")
            break
        
        else:
            print(f"{Fore.RED}Invalid choice. Please enter 1, 2, or 3.{Style.RESET_ALL}")
        
        # Ask if user wants to continue
        continue_choice = input(f"\n{Fore.CYAN}Would you like to try again? (yes/no): {Style.RESET_ALL}").strip().lower()
        if continue_choice not in ['yes', 'y']:
            print(f"\n{Fore.LIGHTMAGENTA_EX}Happy cooking! Come back whenever you need more food inspiration. ❤️{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()