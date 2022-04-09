import { throwError } from './error';

export function assertTrue(
    value: boolean, propertyName: string = 'a property'
): void {
    if (value !== true) throwError(
        `Expected ${propertyName} to be true, ` +
        `but was false instead`
    );
}
