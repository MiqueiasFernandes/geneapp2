export default class LocalFile {
    files = null;

    static inputFile(fn_data: (x: any) => {}, multiple=false) {
        let input: any = document.createElement('input');
        input.type = 'file';
        input.multiple = multiple;
        input.onchange = () => {
            const files: any = new Array()
            for (let index = 0; index < input.files.length; index++) {
                const file = input.files[index];
                files.push(file)
            }
            fn_data(files)
        };
        input.click();
    }

    static importData(fn_data = (x: string) => {}) {
        let input: any = document.createElement('input');
        input.type = 'file';
        input.onchange = () => {
            for (let index = 0; index < input.files.length; index++) {
                const file = input.files[index];
                var reader: any = new FileReader();
                reader.onload = (reader: any) => {
                    fn_data(reader.target.result);
                };
                reader.readAsText(file);
            }
        };
        input.click();
    }

    // static importManyData(fn_data, fn_status = (s: number[], f: string) => { }, fn_choose = (x) => x[0]) {
    //     let input = document.createElement('input');
    //     input.type = 'file';
    //     input.setAttribute("multiple", null);
    //     input.onchange = _ => {
    //         const qtd = input.files.length;
    //         if (qtd < 1) return;
    //         var files: File[] = Array();
    //         for (let index = 0; index < qtd; index++)
    //             files.push(input.files[index]);
    //         fn_status([0, qtd, qtd], null);
    //         const reader = new FileReader();
    //         const processados = [];
    //         var processar = fn_choose(files);
    //         reader.onload = (R) => {
    //             files = files.filter(f => f !== processar);
    //             fn_status([processados.push(processar), qtd, files.length], processar.name);
    //             fn_data(R.target.result, processar.name, files.length);
    //             files.length > 0 && setTimeout(_ => reader.readAsText(processar = fn_choose(files)), 200);
    //         };
    //         reader.readAsText(processar);
    //     };
    //     input.click();
    // }

    static download(filename: string, data: string, type = 'text/txt', end = () => true) {
        const blob = new Blob([data], { type });
        if ((window.navigator as any).msSaveOrOpenBlob) {
            (window.navigator as any).msSaveBlob(blob, filename);
        }
        else {
            const elem = window.document.createElement('a');
            elem.href = window.URL.createObjectURL(blob);
            elem.download = filename;
            document.body.appendChild(elem);
            elem.click();
            document.body.removeChild(elem);
            end()
        }
    }
}