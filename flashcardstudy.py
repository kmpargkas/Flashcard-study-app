import tkinter as tk
from tkinter import messagebox
import json

class Flashcard:
    def __init__(self, term, definition):
        self.term = term
        self.definition = definition

class Deck:
    def __init__(self, name):
        self.name = name
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def get_all_cards(self):
        return self.cards

class FlashcardStudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flashcard Study App")
        self.decks = []

        self.current_deck = None
        self.card_index = 0

        self.deck_name = tk.StringVar()
        self.term = tk.StringVar()
        self.definition = tk.StringVar()
        self.user_answer = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Flashcard Study App", font=("Arial", 14)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        tk.Button(frame, text="Create Deck", command=self.create_deck_window).grid(row=0, column=0, padx=5)
        tk.Button(frame, text="Add Card", command=self.add_card_window).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Study Mode", command=self.select_deck_for_study).grid(row=0, column=2, padx=5)
        tk.Button(frame,text="Manage cards",command=self.edit_card).grid(row=0,column=3,padx=5)
        
        self.listbox = tk.Listbox(self.root, width=50)
        self.listbox.pack(pady=10)

    def create_deck_window(self):
        window = tk.Toplevel(self.root)
        window.title("Create Deck")

        tk.Label(window, text="Deck Name:").pack()
        entry = tk.Entry(window, textvariable=self.deck_name)
        entry.pack()

        def submit():
            name = self.deck_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Deck name cannot be empty.")
                return
            if any(deck.name == name for deck in self.decks):
                messagebox.showerror("Error", "Deck already exists.")
                return
            self.decks.append(Deck(name))
            self.deck_name.set("")
            self.update_listbox()
            window.destroy()

        tk.Button(window, text="Create", command=submit).pack(pady=5)

    def add_card_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Flashcard")

        tk.Label(window, text="Deck Name:").pack()
        deck_entry = tk.Entry(window, textvariable=self.deck_name)
        deck_entry.pack()

        tk.Label(window, text="Term:").pack()
        tk.Entry(window, textvariable=self.term).pack()

        tk.Label(window, text="Definition:").pack()
        tk.Entry(window, textvariable=self.definition).pack()

        def submit():
            deck_name = self.deck_name.get().strip()
            term = self.term.get().strip()
            definition = self.definition.get().strip()
            matched_deck = next((d for d in self.decks if d.name == deck_name), None)
            if not matched_deck:
                messagebox.showerror("Error", "Deck not found.")
                return
            matched_deck.add_card(Flashcard(term, definition))
            self.term.set("")
            self.definition.set("")
            self.deck_name.set("")
            self.update_listbox()
            window.destroy()

        tk.Button(window, text="Add Card", command=submit).pack(pady=5)

    def select_deck_for_study(self):
        window = tk.Toplevel(self.root)
        window.title("Choose Deck")

        tk.Label(window, text="Enter deck name:").pack()
        tk.Entry(window, textvariable=self.deck_name).pack()

        def start():
            name = self.deck_name.get().strip()
            self.current_deck = next((d for d in self.decks if d.name == name), None)
            if not self.current_deck:
                messagebox.showerror("Error", "Deck not found.")
                return
            if not self.current_deck.cards:
                messagebox.showinfo("Info", "Deck is empty.")
                return
            self.card_index = 0
            self.study_mode()
            window.destroy()

        tk.Button(window, text="Start Studying", command=start).pack(pady=5)

    def study_mode(self):
        window = tk.Toplevel(self.root)
        window.title("Study Mode")
        self.user_answer.set("")

        current_card = self.current_deck.cards[self.card_index]

        tk.Label(window, text=f"Term: {current_card.term}", font=("Arial", 12)).pack(pady=5)

        tk.Label(window, text="Your Answer:").pack()
        tk.Entry(window, textvariable=self.user_answer).pack()

        def check_answer():
            if self.user_answer.get().strip().lower() == current_card.definition.lower():
                messagebox.showinfo("Correct", "That's correct!")
            else:
                messagebox.showinfo("Incorrect", f"Correct answer was: {current_card.definition}")
            self.card_index += 1
            if self.card_index < len(self.current_deck.cards):
                window.destroy()
                self.study_mode()
            else:
                messagebox.showinfo("Done", "End of deck!")
                window.destroy()

        tk.Button(window, text="Submit Answer", command=check_answer).pack(pady=5)
    
    def edit_card(self):
        window = tk.Toplevel(self.root)
        window.title("Edit Card")

        deck_name_var = tk.StringVar()
        term = tk.StringVar()
        definition = tk.StringVar()

        tk.Label(window,text="Enter deck name: ").pack()
        user_input = tk.Entry(window,textvariable=deck_name_var)
        user_input.pack()

        tk.Button(window,text="Load cards",command= lambda: load_cards()).pack(pady=5)
        templistbox = tk.Listbox(window,width=50)
        templistbox.pack(pady=5)
        
        def load_cards():
            templistbox.delete(0, tk.END)
            deckname = deck_name_var.get().strip()
            matched = next((d for d in self.decks if d.name==deckname),None)
            if not matched:
                messagebox.showerror("Error","No decks with this name")
                return
            for index, card in enumerate(matched.cards):
                templistbox.insert(tk.END,f"{index+1}. {card.term} - {card.definition}")

            def on_select(event):
                selection = templistbox.curselection()
                if not selection:
                    return
                ind = selection[0]
                deck = next((d for d in self.decks if d.name==deck_name_var.get().strip()),None)
                if deck:
                    sel_card = deck.cards[ind]
                    term.set(sel_card.term)
                    definition.set(sel_card.definition)
            def save_changes():
                selection = templistbox.curselection()
                if not selection:
                    messagebox.showerror("Error","No card selected")
                    return
                ind = selection[0]
                deck = next((d for d in self.decks if d.name==deck_name_var.get().strip()),None)
                if deck:
                    deck.cards[ind].term = term.get().strip()  
                    deck.cards[ind].definition = definition.get().strip()
                    load_cards()
                    self.update_listbox()
                    messagebox.showinfo("Saved","Card updated succesfully")
            
            def delete_card():
                selection = templistbox.curselection()
                if not selection:
                    messagebox.showerror("Error","No card selected")
                ind = selection[0]
                deck = next((d for d in self.decks if d.name==deck_name_var.get().strip()),None)
                if deck:
                    confirm = messagebox.askyesno("Confirmation","Are you sure you want to delete this card?")
                    if confirm:
                        del deck.cards[ind]
                        load_cards()
                        self.update_listbox()
                        term.set("")
                        definition.set("")
                        messagebox.showinfo("Success","Card deleted succesfully")

            tk.Button(window,text="Load cards",command=load_cards).pack(pady=2)
            templistbox.bind('<<ListboxSelect>>', on_select)      

            tk.Label(window,text="Edit term: ").pack()
            tk.Entry(window,textvariable=term).pack()

            tk.Label(window,text="Edit definition: ").pack()
            tk.Entry(window,textvariable=definition).pack()

            tk.Button(window,text="Save changes",command=save_changes).pack(pady=5)  
            tk.Button(window,text="Delete card",command=delete_card).pack(pady=5) 

                    

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for deck in self.decks:
            self.listbox.insert(tk.END, f"Deck: {deck.name} - {len(deck.cards)} cards")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardStudyApp(root)
    root.mainloop()

    
    
 


            







        
        


        


