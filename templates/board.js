
const evtSource = new EventSource("http://localhost:1234/boardEvent", {
    withCredentials: false,
})
// EventSource는 서버에 한 번만 연결해두고,
// 서버가 보내주는 메시지를 계속 자동으로 받는 기능.
// 웹브라우저가 "지켜보고 있다"는 느낌으로 이해하면 된다.
// 서버는 출석 정보가 바뀔 때마다 새로운 메시지를 보내게 된다.

evtSource.addEventListener("update", (event) => {
    // event.data는 서버가 보낸 문자열이다.
    // JSON.parse는 문자열을 실제 사용 가능한 객체로 바꿔준다.
    let data = JSON.parse(event.data)

    // 화면에서 출석표(board)라는 요소를 찾는다.
    // HTML에서 class="board" 로 되어 있는 테이블을 가져온다.
    let board = document.getElementsByClassName("board")[0]
    // 출석표 내용을 전부 지우고, 새로 그릴 준비를 한다
    board.innerHTML = '';

    // 표의 맨 윗줄(학번/이름/출결)을 다시 생성
    buildHeader();

    //각 학생을 순서대로 처리한다.
    Object.keys(data).forEach(id => {

        // 이미 화면에 해당 학생의 줄(tr)이 만들어져 있는지 찾는다.
        // id가 s101인 형식으로 저장해놨다.
        let toUpdate = document.querySelector(`#s${id} td.status`)

        // toUpdate가 없다는 것은 아직 화면에 이 학생 줄이 없다는 뜻.
        // 새 줄을 만들어서 테이블에 추가한다.
        if (toUpdate === null) {
            buildEntry(id, data[id]["name"], data[id]["status"])
        } else {
            // 이미 줄이 있으므로, 출석 칸(status)만 업데이트한다.
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


// 표의 맨 윗부분에 '학번 / 이름 / 출결' 이라는 제목 줄을 만든다.
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

// 학생 1명의 정보를 담은 행을 생성한다.
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

