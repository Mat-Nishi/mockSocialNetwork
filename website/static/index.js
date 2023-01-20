function follow(id){
        fetch('/follow-user', {
            method: 'POST',
            body: JSON.stringify({id}),
        }).then((_res) => {
            window.location.href = "/search";
        });
};