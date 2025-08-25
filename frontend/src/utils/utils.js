export const getLatestUserMessages = (messages) => {
    let lastAssistantIndex = -1;
    for (let i = messages.length - 1; i >= 0; i--) {
        if (messages[i].role !== 'user') {
            lastAssistantIndex = i;
            break;
        }
    }
    return messages.slice(lastAssistantIndex + 1);
}