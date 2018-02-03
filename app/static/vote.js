function submitVote(pollId, option){
    var request = new XMLHttpRequest();
    previous_vote = localStorage.getItem('pollz-' + pollId);
    poll = document.getElementById(pollId);
    update_option = poll.getElementsByClassName('option-' + option)[0].getElementsByClassName('vote-number')[0];
    base_url = '/vote?poll_id=' + pollId + '&option=' + option + '&method=';
    
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status == 200) {
            options = poll.getElementsByClassName('option');
            
            for (var i = 0, n = options.length; i < n; i++) {
                current_vote = options[i].getElementsByClassName('vote-number')[0];
                current_vote.innerText = JSON.parse(request.response)[i].votes;
            }
        }
    };
    
    if (previous_vote === null) {
        url = base_url + 'add';
        request.open('GET', url, true);
        request.send();
        
        update_option.innerText++;
        localStorage.setItem('pollz-' + pollId, option);
        
    } else if (parseInt(previous_vote) !== option){
        url = base_url + 'change&previous_option=' + parseInt(previous_vote);
        request.open('GET', url, true);
        request.send();
        
        previous_option = poll.getElementsByClassName('option-' + previous_vote)[0].getElementsByClassName('vote-number')[0];
        update_option.innerText++;
        previous_option.innerText--;
        localStorage.setItem('pollz-' + pollId, option);
        
    } else {

    }
}

pollNumber = document.getElementsByClassName('poll').length;

for(var i = 0, n = pollNumber; i < n; i++){
    poll = document.getElementsByClassName('poll')[i];
    pollId = poll.id;
    responses = poll.getElementsByClassName('option');
    
    for(var j = 0, m = responses.length; j < m; j++){
        submitButton = poll.getElementsByClassName('submit-vote')[j];
        submitButton.addEventListener('click', submitVote.bind(this, pollId, j));
    }
}
