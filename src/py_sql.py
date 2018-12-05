# -- coding: utf-8 --

import sqlite3
import sys
import os

#Creating edges table
def create_edges(c):
	print("Creating edges")
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
	print("Finished creating edges")
	
#Creating final table
def create_final_table(c):
	print("Creating results table")
	c.execute('''DROP TABLE IF EXISTS Final_Table;''')
	c.execute('''CREATE TABLE  Final_Table(
				page_id INTEGER,
				page_name TEXT,
				page_rank DOUBLE);''')
	print("Finished creating results table")
	
def initialize_final_table(c):
	print("Updating results")
	c.execute('''INSERT INTO Final_Table 
				SELECT id as page_id, title as page_name, page_rank
				FROM (SELECT id, title FROM pages) join edges WHERE id = page_id;''')
	print("Finished updating results")
def reset_final_table(c):
	c.execute('''DELETE FROM Final_Table;''')

				
def get_page_rank_statistic(c, top_number):
	print("Getting top 20 pages")
	c.execute('''SELECT page_name, page_rank FROM Final_Table ORDER BY page_rank DESC LIMIT 20;''')
	return c.fetchall()
	print("Finished getting top 20 pages")
	
#Calculating out_rank values for pages that are not deadends
def update_out_rank(c):
	c.execute('''UPDATE edges SET out_rank = page_rank / out_degree WHERE out_degree != 0;''')
	
#Total entry size
def calculate_entry_size(c):
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

def get_incoming_links(c):
	c.execute('''SELECT in_links FROM edges;''')
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
	c.execute('''UPDATE Final_Table SET page_rank = 0;''')
	return

def select_all_page_ids(c):
	c.execute('''SELECT page_id FROM edges''')
	fetched_id = c.fetchall()
	fetched_id = [i[0] for i in fetched_id]
	return fetched_id
	
#Selecting and returning out ranks
def select_all_out_ranks(c):
	c.execute('''SELECT out_rank FROM edges''')
	fetched_out_rank = c.fetchall()
	fetched_out_rank = [i[0] for i in fetched_out_rank]
	return fetched_out_rank
	
#Map ID's and Out_rank values
def id_rank_mapper(c, page_list, out_ranks):
	dictionary = dict(zip(page_list, out_ranks))
	return dictionary
		
#One iteration of pagerank algorithm
def one_iteration_page_rank(c, beta, num_total, page_list):
	update_out_rank(c)
	reset_pageranks(c)
	
	out_ranks = select_all_out_ranks(c)
	dictionary = id_rank_mapper(c, page_list, out_ranks)
	

	teleport_contribution = (1 - beta)
	leak_contribution = (calculate_total_leak(c) * beta)/ float(num_total)
	
	for i in range (len(page_list)):
		page_rank = teleport_contribution + leak_contribution
		incoming_links = incoming_links_of_page(c, page_list[i]).split("|")
		if(incoming_links[0] != ""):
			for j in range (len(incoming_links)):
				page_rank += dictionary.get(int(incoming_links[j])) * beta
		set_page_rank_of_page(c, page_list[i], page_rank)
		# Some progress info
		percent = 100.0 * i / len(page_list)
		line = '[{0}{1}]'.format('=' * int(percent / 2), ' ' * (50 - int(percent / 2)))
		status = '\r{0:3.0f}%{1} {2:3d}/{3:3d} entries'
		sys.stdout.write(status.format(percent, line, i, len(page_list)))
	
def print_stats(c,top_number):
	stats = get_page_rank_statistic(c, top_number)
	for i in range (top_number):
		print(stats[i],[1])
		
#Page rank algorithm		
def page_rank(c, beta, num_total, iteration_amount, page_list):
	for i in range (iteration_amount):
		one_iteration_page_rank(c, beta, num_total, page_list)
		initialize_final_table(c)
		print_stats(c,20)
		reset_final_table(c)
		
def main():
	conn = sqlite3.connect('sdow.sqlite')
	c = conn.cursor()
	create_edges(c)
	create_final_table(c)
	page_list = select_all_page_ids(c)
	inc_list = get_incoming_links(c)
	num_total = calculate_entry_size(c)
	page_rank(c, 0.9, num_total, 10, page_list)
	
	
	conn.commit()
	conn.close()
	
main()
