from SocialCrawler import NewExtractorData

client_id = "GEQQO0MJPKLUTBIZHERRYQJUCTU5W2MGFAHZKCDB3LYB1GZI"
client_secret = "QMXESMEH1VKEEKUQ0EBXNCJ4IWCK0EYHA0MUHNVBMGSWXRUZ"

file_name = "Brasillog_from_Cuiaba__2016-08-28__2016-09-05.tsv"



test = NewExtractorData.NewExtractor(client_id,client_secret,developer_email="josiel.wirlino@gmail.com",developer_password ="j0sielengenheiro")

indice = 0
# while( indice < 4):

test.settings(mode="v1",
			  out_file_name="cuiaba_final_agosto",
			  out_path_file="/home/wirlino/Documents/Git/SocialCrawler/SocialCrawler/",
			  input_file="/home/wirlino/Documents/Git/SocialCrawler/SocialCrawler/"+file_name			  
			  )

""" We are setting mode to v1 that means the file was created by or Collector or CollectorV2
    output file created will be log_new_york.tsv and will be saved in ./Log/
    the input file ( that contains t.co url ) are localed in ./Log/Brasil/ folder
"""

test.consult_foursquare()
