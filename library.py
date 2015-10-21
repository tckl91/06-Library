class Calendar(object):
    
    def __init__(self):
        """
        The constructor. Sets the date to 0.
        """
        self.date = 0
    
    def get_date(self):
        """
        Returns (as an integer) the current date.
        """
        return self.date
    
    def set_date(self, date):
        self.date=date
        
    def advance(self):
        """
        Increment the date (move ahead to the next day), 
        returns the new date.
        """
        new_calendar=Calendar()
        new_calendar.set_date(self.date+1)
        return new_calendar
    
class Book(object):
    
    def __init__(self, id, title, author):
        """
        The constructor. Saves the provided information. When created, the book is not checked out.
        """
        self.id = id
        self.title = title
        self.author = author
        self.due_date = None
        
    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title
    
    def get_author(self):
        return self.author
    
    def get_due_date(self):
        return self.due_date
    
    def check_out(self, due_date):
        """
        Sets the due date of this Book. Doesn't return anything.
        """
        self.due_date = due_date
    
    def check_in(self):
        """
        Sets the due date of this Book to None. Doesn't return anything.
        """
        self.due_date = None
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "%d: %s, by %s" % (self.id, self.title, self.author)
    
class Patron(object):
    
    def __init__(self, name, library):
        """
        Constructs a patron with the given name, and no books. 
        The patron must also have a reference to the Library object that he/she uses. 
        So that this patron can later be found by name, 
        have a global dictionary which uses the patron's name as the key and the actual Patron object as the value.
        """
        self.name = name;
        self.library = library
        self.books = set()
        
    def get_name(self):
        return self.name
    
    def check_out(self, book):
        """
        Adds this Book object to the set of books checked out by this patron.
        """
        due_date=Calendar()
        due_date.set_date(self.library.get_calendar().get_date()+7)
        book.check_out(due_date)
        self.books.add(book)
        
    def give_back(self, book):
        """
        Removes this Book object from the set of books checked out by this patron. 
        (Since patrons are usually said to "return" books, I wish I could name this method return, 
        but I hope you can see why I can't do that.)
        """
        book.check_in()
        self.books.remove(book)
    
    def get_books(self):
        return self.books
    
    def get_overdue_books(self):
        """
        Returns the set of overdue Book objects checked out to this patron (may be the empty set, set([])).
        """
        result = set()
        for book in self.books:
            if self.library.get_calendar().get_date()>=book.get_due_date().get_date():
                result.add(book)
        return result

class Library(object):
    
    def __init__(self):
        """
        Read in, from the file  collection.txt, a list of (title, author) tuples, 
        Create a Book from each tuple, and save these books in some appropriate data structure of your choice. 
        Give each book a unique id number (starting from 1, not 0). 
        You may have many copies of the "same" book (same title and author), but each will have its own id.

        Create a Calendar object (you should create exactly one of these).
        Define an empty dictionary of patrons. The keys will be the names of patrons and the values will be the corresponding Patron objects.
        Set a flag variable to indicate that the library is not yet open.
        Sets the current patron (the one being served) to None.
        """
        file = open("collection.txt")
        try:
            self.books = []
            book_id = 1
            for book in eval(file.read()):
                self.books.append(Book(book_id, book[0], book[1]))
                book_id += 1
        finally:
            file.close()
        self.calendar = Calendar()
        self.patrons = dict()
        self.opened = False
        self.patron = None
    
    def get_patron(self):
        return self.patron
    
    def get_calendar(self):
        return self.calendar;
    
    def is_open(self):
        return self.opened
        
    def get_books(self):
        return self.books
    
    def open(self):
        """
        If the library is already open, raises an Exception with the message "The library is already open!". 
        Otherwise, starts the day by advancing the Calendar, 
        and setting the flag to indicate that the library is open. ().
        Returns: The string "Today is day n."
        """
        if self.is_open():
            raise Exception("The library is already open!")
        self.calendar=self.calendar.advance()
        self.opened = True
        return "Today is day %d." % self.calendar.get_date()
    
    def find_all_overdue_books(self):
        """
        Returns a nicely formatted, multiline string, listing the names of patrons who have overdue books, 
        and for each such patron, the books that are overdue. Or, it returns the string "No books are overdue.".
        """
        result = ""
        for patron in self.patrons.values():
            books = patron.get_overdue_books()
            if len(books)>0:
                result += "patron %s:\n" % patron.get_name()
                for book in books:
                    result += "  %s\n" % str(book)
        if not result:
            result = "No books are overdue."
        return result
    
    def issue_card(self, name_of_patron):
        """
        Issues a library card to the person with this name. 
        However, no patron should be permitted to have more than one library card.
        Returns either "Library card issued to name_of_patron." or "name_of_patron already has a library card.".
        Possible Exception: "The library is not open.".
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        if self.patrons.get(name_of_patron):
            return "%s already has a library card." % name_of_patron
        else:
            self.patrons[name_of_patron] = Patron(name_of_patron, self)
            return "Library card issued to %s." % name_of_patron
        
    def serve(self, name_of_patron):
        """
        Specifies which patron is about to be served (and quits serving the previous patron, if any). 
        The purpose of this method is so that you don't have to type in the person's name again 
        and again for every book that is to be checked in or checked out. 
        What the method should actually do is to look up the patron's name in the dictionary, 
        and save the returned Patron object in an instance variable of this library.
        Returns either "Now serving name_of_patron." or "name_of_patron does not have a library card.". 
        Possible Exception: "The library is not open."
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        patron = self.patrons.get(name_of_patron)
        if patron:
            self.patron = patron
            return "Now serving %s." % name_of_patron
        else:
            return "%s does not have a library card." % name_of_patron
        
    def find_overdue_books(self):
        """
        Returns a multiline string, each line containing one book (as returned by the book's __str__ method), 
        of the books that have been checked out by the patron currently being served, 
        and which are overdue. If the patron has no overdue books, the value None is returned.
        May raise an Exception with an appropriate message: "The library is not open." "No patron is currently being served."
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        if not self.patron:
            raise Exception("No patron is currently being served.")
        books = self.patron.get_overdue_books()
        if len(books)==0:
            return None
        result = ""
        for book in books:
            result += "%s\n" % str(book)
        return result
    
    def check_in(self, *book_ids):
        """
        The books are being returned by the patron currently being served, 
        so return them to the collection and remove them from the set of books currently checked out to the patron. 
        The book_ids are taken from the list returned by the get_books method in the Patron object. 
        Checking in a Book will involve both telling the Book that it is checked in and returning the Book 
        to this library's collection of available Books.
        If successful, returns "name_of_patron has returned n books.".
        May raise an Exception with an appropriate message:
            "The library is not open."
            "No patron is currently being served."
            "The patron does not have book id."
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        if not self.patron:
            raise Exception("No patron is currently being served.")
        books=[]
        for book_id in book_ids:
            founded=False
            for book in self.patron.get_books():
                if book.get_id()==book_id:
                    books.append(book)
                    founded=True
                    break;
            if not founded:
                raise Exception("The patron does not have book %d." % book_id)
        for book in books:
            self.patron.give_back(book)
            self.books.append(book)
        return "%s has returned %d books." % (self.patron.get_name(),len(books))
        
    def search(self, string):
        """
        Finds those Books whose title or author (or both) contains this string. 
        For example, the string "tact" might return, among other things, the book Contact, by Carl Sagan. 
        The search should be case-insensitive; that is, "saga" would also return this book. 
        Only books which are currently available (not checked out) will be found. 
        If there is more than one copy of a book (with the same title and same author), only one will be found. 
        In addition, to keep from returning too many books, require that the search string be at least 4 characters long.
        Returns one of:
          "No books found."
          "Search string must contain at least four characters."
          A multiline string, each line containing one book (as returned by the book's __str__ method.)
        """
        if string==None or len(string)<4:
            return "Search string must contain at least four characters."
        string=string.lower()
        books=[]
        for book in self.books:
            if string in book.get_title().lower() or string in book.get_author().lower():
                founded=False
                for added_book in books:
                    if book.get_title()==added_book.get_title() and book.get_author()==added_book.get_author():
                        founded=True
                        break;
                if not founded:
                    books.append(book)
        
        if len(books)==0:
            return "No books found."
        result=""
        for book in books:
            result+="%s\n" % str(book)
        return result
    
    def check_out(self, *book_ids):
        """
        Checks out the books to the patron currently being served, 
        or tells why the operation is not permitted. 
        The book_ids could have been found by a recent call to the search method. 
        Checking out a book will involve both telling the book that it is checked out 
        and removing the book from this library's collection of available books. 
        If successful, returns "n books have been checked out to name_of_patron.".
        May raise an Exception with an appropriate message:
            "The library is not open."
            "No patron is currently being served."
            "The library does not have book id."
            "Patron cannot have more than three books." (added October 8)
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        if not self.patron:
            raise Exception("No patron is currently being served.")
        books=set()
        for book_id in book_ids:
            founded=False
            for book in self.books:
                if book.get_id()==book_id:
                    books.add(book)
                    founded=True
                    break;
            if not founded:
                raise Exception("The library does not have book %d." % book_id)
        if len(self.patron.get_books())+len(books)>3:
            raise Exception("Patron cannot have more than three books.")
        for book in books:
            self.patron.check_out(book)
            self.books.remove(book)
        return "%d books have been checked out to %s." % (len(books),self.patron.get_name())
    
    def renew(self, *book_ids):
        """
        Renews the books for the patron currently being served (by setting their due dates to today's date plus 7) 
        or tells why the operation is not permitted.
        If successful, returns "n books have been renewed for name_of_patron.".
        May raise an Exception with an appropriate message:
            "The library is not open."
            "No patron is currently being served."
            "The patron does not have book id."
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        if not self.patron:
            raise Exception("No patron is currently being served.")
        books=[]
        for book_id in book_ids:
            founded=False
            for book in self.patron.get_books():
                if book.get_id()==book_id:
                    books.append(book)
                    founded=True
                    break;
            if not founded:
                raise Exception("The patron does not have book %d." % book_id)
        for book in books:
            self.patron.check_out(book)
        return "%d books have been renewed for %s." % (len(books),self.patron.get_name())
    
    def close(self):
        """
        Shut down operations and go home for the night. 
        None of the other operations (except quit) can be used when the library is closed.
        If successful, returns the string "Good night.".
            May raise an Exception with the message "The library is not open."
        """
        if not self.is_open():
            raise Exception("The library is not open.")
        self.opened=False
        self.patron=None
        return "Good night."
    
    def quit(self):
        """
        The mayor, citing a budget crisis, has stopped all funding for the library. Can happen at any time. 
        Returns the string "The library is now closed for renovations.".
        """
        return "The library is now closed for renovations."    
    
def main():
    library=Library()
    quited=False
    while not quited:
        tip="#"
        if library.is_open():
            tip="$"
            if library.get_patron():
                tip=tip+"(%s)" % library.get_patron().get_name()
        inputs=input(tip+" ").split()
        cmd=inputs[0].lower()
        try:
            ret=None
            if cmd=="open":
                ret=library.open()
            elif cmd=="overdue":
                ret=library.find_all_overdue_books()
            elif cmd=="card":
                if len(inputs)>1:
                    ret=library.issue_card(inputs[1])
            elif cmd=="serve":
                if len(inputs)>1:
                    ret=library.serve(inputs[1])
            elif cmd=="checkin":
                if len(inputs)>1:
                    ret=eval("library.check_in("+",".join(inputs[1:])+")")
            elif cmd=="checkout":
                if len(inputs)>1:
                    ret=eval("library.check_out("+",".join(inputs[1:])+")")
            elif cmd=="renew":
                if len(inputs)>1:
                    ret=eval("library.renew("+",".join(inputs[1:])+")")
            elif cmd=="search":
                if len(inputs)>1:
                    ret=library.search(inputs[1])
            elif cmd=="close":
                ret=library.close()
            elif cmd=="quit":
                quited=True
            if ret:
                print(ret)
        except:
            import traceback
            traceback.print_exc()
            
    print(library.quit())
    
if __name__ == "__main__":
    main()    
