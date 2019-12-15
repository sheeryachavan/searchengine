
# requirement.txt

Open two separate terminals:
Terminal1
Terminal2

Terminal1:
1. Navigate to frontend folder
2. Run "npm install"
3. After the dependencies are installed, start the app by "npm start"
4. The frontend is now up and the app would be visible on the browser at "http://localhost:3000"
# <Load app on web>
5. Download and install `ngrok` from `https://ngrok.com/`
6. Hit command `$ ./ngrok http 3000`
7. Hit the displayed link

# Backend is running on http://3.83.65.164
# To run backend locally...
Terminal2:
1. Navigate to frontend folder - `$ cd ./frontend`
2. Open `package.json` file
3. Change the proxy to `http://localhost:<port>`
4. Open `apiClient.js` in `src` directory
5. Change `const BASE_URI = 'http://3.83.65.164'` to `const BASE_URI = 'http://localhost:<port>'`
6. Navigate to backend folder - `$ cd ../../backend`
7. install all requirements - $ pip install -r requirements.txt
8. Run "python3 app.py"
9. The backend of the app is now up on `http://localhost:<port>`

### Note: The crawler, scrapper and inverted-index scripts are provided in `backend directory