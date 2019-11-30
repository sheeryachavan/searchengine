import axios from 'axios';
const BASE_URI = 'http://127.0.0.1:5000';
const client = axios.create({
    baseURL: BASE_URI,
    json: true
});
class APIClient {



    getResults(query) {

        return query ? this.perform('get', '/results', query) : this.perform('get', '/');
    }

    async perform(method, resource, data) {
        return client({
            method,
            url: resource,
            data
        }).then(resp => {
            return resp.data ? resp.data : [];
        })
    }
}

export default APIClient;