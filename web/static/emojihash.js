window.emoji = function(hashedData, size) {
    size = size === undefined ? -1 : size;
    if (size <= 0) {
        size = hashedData.length;
    } else {
        size = Math.min(size, hashedData.length);
    }
    var result = [];
    for (let i = 0; i < size; i++) {
        var code = hashedData[i].toString(16);
        result.push(String.fromCodePoint(parseInt("1f4"+code, 16)));
    }
    return result;
}