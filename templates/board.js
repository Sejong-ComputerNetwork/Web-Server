
const evtSource = new EventSource("http://localhost:1234/boardEvent", {
    withCredentials: false,
})

evtSource.addEventListener("update", (event) => {
    let data = JSON.parse(event.data)

    let board = document.getElementsByClassName("board")[0]
    board.innerHTML = '';
    buildHeader();

    Object.keys(data).forEach(id => {
        console.log(id)
        console.log(data[id]["name"])
        console.log(data[id]["status"])
        let toUpdate = document.querySelector(`#s${id} td.status`)
        if (toUpdate === null) {
            buildEntry(id, data[id]["name"], data[id]["status"])
        } else {
            if (data[id]["status"]) {
                toUpdate.classList.remove("didNotAttend")
                toUpdate.classList.add("didAttend")
                toUpdate.innerHTML = "O"

            } else {
                toUpdate.classList.add("didNotAttend")
                toUpdate.classList.remove("didAttend")
                toUpdate.innerHTML = "X"
            }
        }
    });
});

function buildHeader() {
    let board = document.getElementsByClassName("board")[0]
    let headerRow = document.createElement("tr")
    headerRow.class = "header"

    let studentId = document.createElement("td")
    studentId.innerHTML = "학번"

    let studentName = document.createElement("td")
    studentName.innerHTML = "이름"

    let studentStatus = document.createElement("td")
    studentStatus.innerHTML = "출결"

    headerRow.appendChild(studentId)
    headerRow.appendChild(studentName)
    headerRow.appendChild(studentStatus)

    board.appendChild(headerRow)
}

function buildEntry(id, name, status) {
    let board = document.getElementsByClassName("board")[0]
    let newEntry = document.createElement("tr")
    newEntry.id = `s${id}`

    let studentId = document.createElement("td")
    studentId.classList.add("sid")
    studentId.innerHTML = id

    let studentName = document.createElement("td")
    studentName.classList.add("name")
    studentName.innerHTML = name

    let studentStatus = document.createElement("td")
    studentStatus.classList.add("status")
    studentStatus.innerHTML = status

    if (status) {
        studentStatus.classList.add("didAttend")
        studentStatus.innerHTML = "O"
    } else {
        studentStatus.classList.add("didNotAttend")
        studentStatus.innerHTML = "X"
    }

    newEntry.appendChild(studentId)
    newEntry.appendChild(studentName)
    newEntry.appendChild(studentStatus)

    board.appendChild(newEntry)
}

