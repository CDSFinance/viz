""" 
Given a raw file from the S3 bucket, and the predicted prices for each date from the neural network,
output a formatted csv file that will be more easily fed into D3 for visualization.

Usage: python [AAPL.csv] [NeuralOutput.csv] [AAPL_Formatted]

Raw file and predicted file must have the same number of lines or else exception witll be thrown 
"""

from boto.s3.connection import S3Connection 

# globals
fileType = ".csv"

def read_s3():
	aws_connection = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
	bucket = aws_connection.get_bucket("cdsquantfinance")
	for file_key in bucket.list():
		print file_key.name


if __name__=="__main__":

	read_s3()

	raw_data = open("AAPL" + fileType)
	predicted = open("AAPL" + "_predicted" + fileType)
	output = open("AAPL" + "_formatted" + fileType, "w")

	# the first row is the column names. Throw them away
	raw_data.readline();
	predicted.readline();	

	# write the column names
	output.write("Date,Close,Predicted\n")

	for line in raw_data:

		# parse raw data
		data = line.split(",")
		date, close = data[0], data[4]

		# parse predicted data
		predicted_line = predicted.readline();
		date2, predicted_price = predicted_line.split(",")

		if date != date2: raise # should not ever happen

		res = ",".join([date,close,predicted_price])
		output.write(res)


	raw_data.close()
	predicted.close()
	output.close()
