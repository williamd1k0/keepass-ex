var typed_arrays = [
    Int8Array,
    Uint8Array,
    Int16Array,
    Uint16Array,
    Int32Array,
    Uint32Array,
    Float32Array,
    Float64Array
];

typed_arrays.forEach(function (typed_array) {
    if (typed_array.prototype.slice) { return; }

    typed_array.prototype.slice = function (begin, end) {
        var len = this.length;;
        var size;
        var start = begin || 0;

        start = (start >= 0) ? start : Math.max(0, len + start);
        end = end || len;

        var up_to = (typeof end == 'number') ? Math.min(end, len) : len;
        if (end < 0) up_to = len + end;

        // actual expected size of the slice
        size = up_to - start;

        // if size is negative it should return an empty array
        if (size <= 0) size = 0;

        var typed_array_constructor = this.constructor;
        var cloned = new typed_array_constructor(size);

        for (var i = 0; i < size; i++) {
            cloned[i] = this[start + i];
        }

        return cloned;
    };
});

if (!Uint8Array.prototype.join) {
    Object.defineProperty(Uint8Array.prototype, 'join', {
        value: Array.prototype.join
    });
}