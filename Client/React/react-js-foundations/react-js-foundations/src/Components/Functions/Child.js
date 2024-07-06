const Child = props => {
    let companies = [];

    const [platform , experience] = ['Dotnet' , '13'];

    if(props.companies){
        companies = props.companies.map((company, index) => 
            <p key={index}> Worked in {company} </p>
    );
    }
    return(
    <>
        <span style={{backgroundColor:"lightblue"}}> this is my name {props.name} and 
        age is {props.age} in platform as {platform} and with experience as {experience} </span>      
          <p> with work experience as  </p>{companies}         
    </>
    )
}

export default Child;


 