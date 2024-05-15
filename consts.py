SQL = """
            SELECT books.id, books.title, authors.name
            FROM books
            JOIN authors ON books.author_id = authors.id
        """
