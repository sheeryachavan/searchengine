import axios from 'axios';
const BASE_URI = 'http://3.83.65.164';
// const BASE_URI = 'http://172.31.53.78';
// const BASE_URI = 'http://localhost:5000';
const client = axios.create({
    baseURL: BASE_URI,
    json: true,
    data: {}
});
class APIClient {



    getResults(query) {
        if (query)
            return this.perform('POST', '/results', query)
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