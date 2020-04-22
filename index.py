from flask import Flask,render_template,request
import subprocess,os
from subprocess import PIPE

app = Flask(__name__)

#route for the main page.
@app.route('/')
def Compiler():
	check=''
	return render_template('home.html',check=check)

#route for the submit page to show the output/error of the c program.
@app.route('/submit',methods=['GET','POST'])
def submit():
	if request.method=='POST':

		#Getting input(code and input for program) and checkbox value from the form.
		code=request.form['code']
		inp=request.form['input']
		chk=request.form.get('check')

		#Checking if the checkbox is checked or not.
		if  not chk=='1':
			#If checkbox was not ckecked then the input field will be empty and checkbox will be unchecked. 
			inp=""
			check=''
		else:
			##If checkbox was ckecked then the input field will stay the same and checkbox will be checked.
			check='checked'	

		#calling the function to compile and execute the c program.	
		output=complier_output(code,inp,chk)
	#return render_tempelate to 	
	return render_template('home.html',code=code,input=inp,output=output,check=check)

def complier_output(code,inp,chk):
	#checking if a file already exists or not in no the create one.
	if not os.path.exists('Try.c'):
		os.open('Try.c',os.O_CREAT)
	#creating a file descriptor to write in to the file.	
	fd=os.open("Try.c",os.O_WRONLY)
	#truncate the content of the file to 0 bytes so that there is no overwriting in any way using the write operation.
	os.truncate(fd,0)
	#encode the string into bytes.
	fileadd=str.encode(code)
	#write to the file.
	os.write(fd,fileadd)
	#close the file descriptor.
	os.close(fd)
	#Compiling the c program file and retrieving the error if any. 
	s=subprocess.run(['gcc','-o','new','Try.c'],stderr=PIPE,)
	#storing the value returned by return code.
	check=s.returncode
	#checking whether program compiled succesfully or not.
	if check==0:
		#cheking whether input for program is enabled or not.
		if chk=='1':
			#executing the program with input.
			r=subprocess.run(["new.exe"],input=inp.encode(),stdout=PIPE)
		else:
			#executing the program without input.
			r=subprocess.run(["new.exe"],stdout=PIPE)
		#return the output of the program.	
		return r.stdout.decode("utf-8")
	else:
		#return the error if the program did not compile successfully
		return s.stderr.decode("utf-8")


if __name__=='__main__':
	app.run(debug=True)