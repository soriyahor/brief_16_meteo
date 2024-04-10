document.getElementById('btn-submit').addEventListener('click', async (event) => {
    event.preventDefault();
    const name_city = document.getElementById('name_city').value;
    const date = document.getElementById('date').value;
    const hour = document.getElementById('hour').value;

    try {
        const response = await fetch(`http://soriyab16-fastfront.francecentral.azurecontainer.io:8020/forecast?city=${name_city}&date=${date}&hour=${hour}`);
        // const response = await fetch(`http://localhost:8020/forecast?city=${name_city}&date=${date}&hour=${hour}`);
      
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        const audio = new Audio(url);
        audio.controls = true;
        document.body.appendChild(audio);

    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
});
