export function throwError<T = never>(error?: string | Error): T {
    throw error instanceof Error ? error : new Error(error);
}

export function catchError<T = any>(fn: () => T): T | undefined {
    try { return fn(); }
    catch { return undefined; }
}

export function expectError<E = any>(fn: () => any): E {
    let result: any;

    try {
        result = fn();
    } catch (error) {
        return error as E;
    }

    throw result;
}

export async function expectErrorAsync<E = any>(
    fn: () => Promise<any>
): Promise<E> {
    let result: any;

    try {
        result = await fn();
    } catch (error) {
        return error as E;
    }

    throw result;
}
