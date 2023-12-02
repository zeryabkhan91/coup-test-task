document.getElementById("playForm").addEventListener("submit", function (event) {
  event.preventDefault();

  fetch("{% url 'create_game' %}", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": "{{ csrf_token }}",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("gameId").value = data.game_id;
      document.getElementById("playForm").submit();
    });
});
