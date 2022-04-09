export function timeoutAsync<T>(
    promise: Promise<T>, millis: number
): Promise<T> {
    const timeout = new Promise<T>((_resolve, reject) =>
        setTimeout(() => reject('Timed out'), millis)
    );
    return Promise.race([promise, timeout]);
}
