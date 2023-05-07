function emoji(hashedData, size = -1) {
    if (size <= 0) {
        size = hashedData.length;
    } else {
        size = Math.min(size, hashedData.length);
    }
    const result = [];
    for (let i = 0; i < size; i++) {
        const code = hashedData[i].toString(16);
        result.push(String.fromCodePoint(parseInt(`1f4${code}`, 16)));
    }
    return result;
}