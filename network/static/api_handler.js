export default class ApiHandler {

    Get(url, token) {
        fetch(url, {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch" + response.statusText);
                }
                console.log(response)
                return response.json()
            })
            .then(data => {
                console.log(data);
            })
    }
    Post(url, body, token) {
        fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                },
                body: JSON.stringify(body),
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to fetch" + response.statusText)
                }
                console.log(response)
                return response.json()
            })
            .then(data => {
                console.log(data)
            })
    }
}