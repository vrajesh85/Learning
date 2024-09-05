import {useState} from 'react';

function RestResponse(){
    const [repos,setRepos] = useState([]);
    const URL = 'https://api.github.com/users/facebook/repos'
    const [status,setStatus] = useState();

    const getRepos = () => {
                        fetch(URL)
                        .then(response => response.json())
                        .then(data => { setRepos(data);})
                        .then(setStatus("fetched"))
                        .catch(error => console.error(error))
    }

    const logRepos = () => {
            console.log(repos);
    }

return(
    <>
        <button onClick={getRepos}>{status?"Fetched All":"Fetch Repos"}</button>
        <button onClick={logRepos}>Log Repos</button>
    </>
)
}

export default RestResponse;