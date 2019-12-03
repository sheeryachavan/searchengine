import axios from 'axios';
const BASE_URI = 'http://127.0.0.1:5000';
const client = axios.create({
    baseURL: BASE_URI,
    json: true,
    data:{}
});
class APIClient {



    getResults(query) {
        if (query)
            return this.perform('post', 'http://35.170.249.243:5000/results', query)
        else {
            this.perform('get', '/');
        }
    }

    async perform(method, resource, data) {
        return client({
            method,
            url: resource,
            data: data
        }).then(resp => {
            console.log(resp);
            return resp.data ? resp.data : [];
        })
    }
}

export default APIClient;