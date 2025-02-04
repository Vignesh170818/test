export async function downloadFile(content, fileName, mimeType) {
    const blob = new Blob([content], { type: mimeType });
    const reusableLink = document.createElement('a');
    reusableLink.href = window.URL.createObjectURL(blob);
    reusableLink.download = fileName;
    reusableLink.click();
    window.URL.revokeObjectURL(reusableLink.href);
}

export async function downloadWord(content, fileName) {
    await downloadFile(content, fileName, 'application/msword');
}

export async function downloadText(content, fileName) {
    await downloadFile(content, fileName, 'text/plain');
}

export async function downloadPDF(content, fileName) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF('p', 'pt', 'a4');

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    doc.setFont("helvetica", "normal");
    doc.setFontSize(12);

    const lines = content.split('\n');
    let marginTop = 40;
    const marginLeft = 40;
    const lineHeight = 20;

    for (let line of lines) {
        if (marginTop + lineHeight > pageHeight) {
            doc.addPage();
            marginTop = 40;
        }

        let fontSize = 12;
        let fontStyle = "normal";
        let text = line;

        if (line.startsWith('# ')) {
            fontStyle = "bold";
            fontSize = 14;
            text = line.substring(2);
        } else if (line.startsWith('## ')) {
            fontStyle = "bold";
            text = line.substring(3);
        }

        if (doc.internal.getFontSize() !== fontSize || doc.internal.getFont().fontStyle !== fontStyle) {
            doc.setFontSize(fontSize);
            doc.setFont("helvetica", fontStyle);
        }

        const wrappedLines = doc.splitTextToSize(text, pageWidth - marginLeft * 2);

        for (let wrappedLine of wrappedLines) {
            if (marginTop + lineHeight > pageHeight) {
                doc.addPage();
                marginTop = 40;
            }
            doc.text(wrappedLine, marginLeft, marginTop);
            marginTop += lineHeight;
        }
    }
    doc.save(fileName);
}
