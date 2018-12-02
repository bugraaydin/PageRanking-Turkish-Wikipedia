# -- coding: utf-8 --

import sqlite3

#Creating edges table
def create_edges(c):
	#Creating the table edges using prepared table links
	c.execute('''DROP TABLE IF EXISTS edges;''')
	c.execute('''
	CREATE TABLE IF NOT EXISTS edges (
		page_id INTEGER PRIMARY KEY,
		out_degree INTEGER NOT NULL,
		page_rank DOUBLE NOT NULL,
		out_rank DOUBLE NOT NULL,
		in_links TEXT NOT NULL
	);
	''')
	c.execute('''INSERT INTO edges
		SELECT id as page_id, outgoing_links_count as out_degree, 1.0 as page_rank, 0.0 as out_rank, incoming_links as in_links
		FROM links;''')

#Creating final table
def create_final_table(c):
	c.execute('''DROP TABLE IF EXISTS Final_Table;''')
	c.execute('''CREATE TABLE  Final_Table(
				page_id INTEGER,
				page_name TEXT,
				page_rank DOUBLE);''')
	
def update_final_table(c):
	c.execute('''INSERT INTO Final_Table 
				SELECT id as page_id, title as page_name, page_rank
				FROM (SELECT id, title FROM pages) join edges WHERE id = page_id;''')

				
def get_page_rank_statistic(c, top_number):
	c.execute('''SELECT page_name, page_rank FROM Final_Table ORDER BY page_rank DESC LIMIT 20;''')
	return c.fetchall()
#Calculating out_rank values for pages that are not deadends
def update_out_rank(c):
	c.execute('''UPDATE edges SET out_rank = page_rank / out_degree WHERE out_degree != 0;''')
	
#Total entry size
def calcualte_entry_size(c):
	#Number of total pages
	c.execute('''SELECT COUNT(page_id) FROM edges;''')
	num_total = c.fetchone()[0]
	return num_total

#Calculate leak
def calculate_total_leak(c):
	#Summation of page_ranks of pages that has no out going links
	c.execute('''SELECT COUNT(page_rank) FROM edges WHERE out_degree = 0;''')
	total_leak = c.fetchone()[0]
	return total_leak


#Return incoming links of a page, chance the page_id with corresponding one	
def incoming_links_of_page(c, page_id):
	c.execute('''SELECT in_links FROM edges WHERE page_id = (?);''', (page_id,))
	return c.fetchone()[0]
	
#Return the out_rank given a page_id, change page_id with a corresponding one	
def out_rank_of_page(c, page_id):
	#Return the out_rank given a page_id, change page_id with a corresponding one
	c.execute('''SELECT out_rank FROM edges WHERE page_id = (?);''', (page_id,))
	return c.fetchone()[0]

#Set a pagerank of the column given page_id and value
def set_page_rank_of_page(c, page_id, value):
	#Set a pagerank of the column given page_id and value
	c.execute('''UPDATE edges SET page_rank = (?) WHERE page_id = (?)''', (value, page_id))
	return

#Set a pagerank of the column given page_id and value
def reset_pageranks(c):
	c.execute('''UPDATE edges SET page_rank = 0;''')
	return
	
#Selecting and returning all page ids
def select_all_page_ids_and_out_ranks(c):
	c.execute('''SELECT page_id FROM edges''')
	fetched_id = c.fetchall()
	fetched_id = [i[0] for i in fetched_id]
	c.execute('''SELECT out_rank FROM edges''')
	fetched_out_rank = c.fetchall()
	fetched_out_rank = [i[0] for i in fetched_out_rank]
	return fetched_id, fetched_out_rank
	
#Map ID's and Out_rank values
def id_rank_mapper(c, page_list, out_ranks):
	dictionary = dict(zip(page_list, out_ranks))
	return dictionary

#One iteration of pagerank algorithm
def one_iteration_page_rank(c, beta, num_total):
	update_out_rank(c)
	reset_pageranks(c)
	page_list, out_ranks = select_all_page_ids_and_out_ranks(c)
	dictionary = id_rank_mapper(c, page_list, out_ranks)
	
	
	teleport_contribution = (1 - beta)
	leak_contribution = (calculate_total_leak(c) * beta)/ float(num_total)
	print(leak_contribution ,"~~~~")
	print(calculate_total_leak(c), "~~~~")
	for i in range (len(page_list)):
		page_rank = teleport_contribution + leak_contribution
		incoming_links = incoming_links_of_page(c, page_list[i]).split("|")
		if(incoming_links[0] != ""):
			for j in range (len(incoming_links)):
				page_rank += dictionary.get(int(incoming_links[j])) * beta
		set_page_rank_of_page(c, page_list[i], page_rank)

		
def print_stats(c,top_number):
	stats = get_page_rank_statistic(c, top_number)
	for i in range (top_number):
		print(stats[i][0],"~",stats[i],[1])
#Page rank algorithm		
def page_rank(c, beta, num_total, iteration_amount):
	for i in range (iteration_amount):
		one_iteration_page_rank(c, beta, num_total)
		update_final_table(c)
		print_stats(c,20)
		
def main():
	conn = sqlite3.connect('sdow.sqlite')
	c = conn.cursor()
	create_edges(c)
	create_final_table(c)
	num_total = calcualte_entry_size(c)
	page_rank(c, 0.8, num_total, 4)
	
	
	conn.commit()
	conn.close()
main()
