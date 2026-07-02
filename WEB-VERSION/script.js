// Web version script for THE ARCHITECTURE OF SHADOWS

const volumes = {
    master: [
        { name: "Volume I: The Foundations", path: "../MASTER-EDITION/VOLUME-I-THE-FOUNDATIONS" },
        { name: "Volume II: The Players", path: "../MASTER-EDITION/VOLUME-II-THE-PLAYERS" },
        { name: "Volume III: The Processes", path: "../MASTER-EDITION/VOLUME-III-THE-PROCESSES" },
        { name: "Volume IV: The Consequences", path: "../MASTER-EDITION/VOLUME-IV-THE-CONSEQUENCES" },
        { name: "Volume V: The Alternatives", path: "../MASTER-EDITION/VOLUME-V-THE-ALTERNATIVES" },
        { name: "Volume VI: Public Perception", path: "../MASTER-EDITION/VOLUME-VI-PUBLIC-PERCEPTION" },
        { name: "Volume VII: Global Perspectives", path: "../MASTER-EDITION/VOLUME-VII-GLOBAL-PERSPECTIVES" },
        { name: "Volume VIII: Special Topics", path: "../MASTER-EDITION/VOLUME-VIII-SPECIAL-TOPICS" },
        { name: "Volume IX: Hidden Architecture", path: "../MASTER-EDITION/VOLUME-IX-HIDDEN-ARCHITECTURE", hidden: true },
        { name: "Volume X: The Resistance", path: "../MASTER-EDITION/VOLUME-X-THE-RESISTANCE" },
        { name: "Volume XI: Synthesis and Integration", path: "../MASTER-EDITION/VOLUME-XI-SYNTHESIS-AND-INTEGRATION" },
        { name: "Volume XII: Conclusion and Integration", path: "../MASTER-EDITION/VOLUME-XII-CONCLUSION-AND-INTEGRATION" },
        { name: "Volume XIII: Appendices and References", path: "../MASTER-EDITION/VOLUME-XIII-APPENDICES-AND-REFERENCES" },
        { name: "Volume XIV: Hidden Messages", path: "../MASTER-EDITION/VOLUME-XIV-HIDDEN-MESSAGES", hidden: true },
        { name: "Volume XV: Esoteric Knowledge", path: "../MASTER-EDITION/VOLUME-XV-ESOTERIC-KNOWLEDGE", hidden: true },
        { name: "Volume XVI: Advanced Topics", path: "../MASTER-EDITION/VOLUME-XVI-ADVANCED-TOPICS", hidden: true }
    ],
    student: [
        { name: "Volume I: The Foundations", path: "../STUDENT-EDITION/VOLUME-I-THE-FOUNDATIONS" },
        { name: "Volume II: The Players", path: "../STUDENT-EDITION/VOLUME-II-THE-PLAYERS" },
        { name: "Volume III: The Processes", path: "../STUDENT-EDITION/VOLUME-III-THE-PROCESSES" },
        { name: "Volume IV: The Consequences", path: "../STUDENT-EDITION/VOLUME-IV-THE-CONSEQUENCES" },
        { name: "Volume V: The Alternatives", path: "../STUDENT-EDITION/VOLUME-V-THE-ALTERNATIVES" },
        { name: "Volume VI: Public Perception", path: "../STUDENT-EDITION/VOLUME-VI-PUBLIC-PERCEPTION" },
        { name: "Volume VII: Global Perspectives", path: "../STUDENT-EDITION/VOLUME-VII-GLOBAL-PERSPECTIVES" },
        { name: "Volume VIII: Special Topics", path: "../STUDENT-EDITION/VOLUME-VIII-SPECIAL-TOPICS" },
        { name: "Volume X: The Resistance", path: "../STUDENT-EDITION/VOLUME-X-THE-RESISTANCE" },
        { name: "Volume XI: Synthesis and Integration", path: "../STUDENT-EDITION/VOLUME-XI-SYNTHESIS-AND-INTEGRATION" },
        { name: "Volume XII: Conclusion and Integration", path: "../STUDENT-EDITION/VOLUME-XII-CONCLUSION-AND-INTEGRATION" },
        { name: "Volume XIII: Appendices and References", path: "../STUDENT-EDITION/VOLUME-XIII-APPENDICES-AND-REFERENCES" }
    ]
};

let currentEdition = null;
let currentVolume = null;

function showEdition(edition) {
    currentEdition = edition;
    document.querySelector('.welcome').classList.add('hidden');
    document.getElementById('volume-nav').classList.remove('hidden');
    document.getElementById('chapter-content').classList.add('hidden');
    
    const volumeList = document.getElementById('volume-list');
    volumeList.innerHTML = '';
    
    volumes[edition].forEach((volume, index) => {
        const card = document.createElement('div');
        card.className = 'volume-card';
        card.innerHTML = `
            <h3>${volume.name}</h3>
            <p>${volume.hidden ? '<span class="hidden-flag">Hidden Content</span>' : 'Standard Content'}</p>
        `;
        card.onclick = () => showVolume(index);
        volumeList.appendChild(card);
    });
}

function showVolume(index) {
    currentVolume = index;
    const volume = volumes[currentEdition][index];
    
    // For a full implementation, this would load and display chapters
    // For now, show a placeholder
    document.getElementById('volume-nav').classList.add('hidden');
    document.getElementById('chapter-content').classList.remove('hidden');
    
    const display = document.getElementById('chapter-display');
    display.innerHTML = `
        <h1>${volume.name}</h1>
        <p>Chapter loading would be implemented here.</p>
        <p>Path: ${volume.path}</p>
        <p><em>Note: Full chapter loading requires a backend server or static site generator.</em></p>
    `;
}

function backToVolumes() {
    document.getElementById('volume-nav').classList.remove('hidden');
    document.getElementById('chapter-content').classList.add('hidden');
}
