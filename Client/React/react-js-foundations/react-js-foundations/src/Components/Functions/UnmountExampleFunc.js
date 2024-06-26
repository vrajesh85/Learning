import {useState, useEffect} from 'react';

const UnmountExampleFunc = () => {

    const [secs, setSeconds] = useState(0);

   useEffect(() => {
        const interval = setInterval(() => {
            setSeconds(prevSeconds => prevSeconds + 1)
        } , 1000);


        return () => {
            clearInterval(interval);
        }
   },[]);
   
   return(
        <div>
            The interval with function component is {secs}
        </div>
   );
    
}

export default UnmountExampleFunc;