export function range(start: number, stop: number): Array<number> {
    const result = [];
    for (let i = start; i < stop; i++) {
        result.push(i);
    }
    return result;
}

export function split<T>(array: Array<T>, size: number): Array<Array<T>> {
    const chunkLength = Math.ceil(array.length / size);
    const chunks = [];
    for (let i = 0; i < chunkLength; i++) {
        chunks.push(array.slice(i * size, (i + 1) * size));
    }
    return chunks;
}
