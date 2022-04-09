type EnvName = 'test' | 'dev' | 'prod';

type AppConfig = {
    name: EnvName
};

function getCurrentEnvName(): EnvName {
    const envName = process.env.NODE_ENV || 'dev';
    switch (envName) {
        case 'development': return 'dev';
        case 'production': return 'prod';
        default: return envName as EnvName;
    }
}

const currentEnv = getCurrentEnvName();
export const config: AppConfig = {
    name: currentEnv
};
