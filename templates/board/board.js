
const evtSource = new EventSource("http://localhost:1234/boardEvent", {
    withCredentials: false,
})

evtSource.addEventListener("update", (event) => {
    let data = JSON.parse(event.data)

    Object.keys(data).forEach(id => {
        console.log(id)
        console.log(data[id])
        let toUpdate = document.querySelector(`#s${id} span.status`)
        if (toUpdate === null) {
            buildEntry(id, data[id])
        } else {
            toUpdate.innerHTML = data[id]
        }
    });
});


function buildEntry(id, status) {
    let board = document.getElementsByClassName("board")[0]
    let newEntry = document.createElement("li")
    newEntry.id = `s${id}`

    let name = document.createElement("span")
    name.classList.add("name")
    name.innerHTML = id

    let buffer = document.createElement("span")
    buffer.classList.add("buffer")
    buffer.innerHTML = " : "

    let statusSpan = document.createElement("span")
    statusSpan.classList.add("status")
    statusSpan.innerHTML = status

    newEntry.appendChild(name)
    newEntry.appendChild(buffer)
    newEntry.appendChild(statusSpan)

    board.appendChild(newEntry)
}

