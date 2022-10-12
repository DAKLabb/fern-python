from fern_python.codegen import AST, Filepath, Project
from fern_python.generator_exec_wrapper import GeneratorExecWrapper
from fern_python.source_file_generator import SourceFileGenerator

from ..context import FastApiGeneratorContext
from ..external_dependencies import FastAPI
from .service_initializer import ServiceInitializer


class RegisterFileGenerator:
    _MODULE_NAME = "register"
    _REGISTER_FUNCTION_NAME = "register"
    _REGISTER_SERVICE_FUNCTION_NAME = "__register_service"
    _APP_PARAMETER_NAME = "app"
    _SERVICE_PARAMETER_NAME = "service"

    def __init__(self, context: FastApiGeneratorContext):
        self._context = context
        self._service_initializers = [
            ServiceInitializer(context=context, service=service) for service in self._context.ir.services.http
        ]

    def generate_registry_file(self, project: Project, generator_exec_wrapper: GeneratorExecWrapper) -> None:
        with SourceFileGenerator.generate(
            project=project,
            generator_exec_wrapper=generator_exec_wrapper,
            filepath=Filepath(
                directories=(self._context.filepath_creator.generate_filepath_prefix()),
                file=Filepath.FilepathPart(module_name=RegisterFileGenerator._MODULE_NAME),
            ),
        ) as source_file:
            source_file.add_declaration(declaration=self._get_register_method(), should_export=False)
            source_file.add_declaration(declaration=self._get_register_service_method(), should_export=False)
            source_file.add_declaration(declaration=self._get_register_validators_method(), should_export=False)

    def _get_register_method(self) -> AST.FunctionDeclaration:
        return AST.FunctionDeclaration(
            name=RegisterFileGenerator._REGISTER_FUNCTION_NAME,
            signature=AST.FunctionSignature(
                parameters=[
                    AST.FunctionParameter(name=RegisterFileGenerator._APP_PARAMETER_NAME, type_hint=FastAPI.FastAPI),
                ],
                named_parameters=[
                    service_initializer.get_register_parameter() for service_initializer in self._service_initializers
                ],
                return_type=AST.TypeHint.none(),
            ),
            body=AST.CodeWriter(self._write_register_method_body),
        )

    def _write_register_method_body(self, writer: AST.NodeWriter) -> None:
        for service_initializer in self._service_initializers:
            writer.write_node(
                node=FastAPI.include_router(
                    app_variable=RegisterFileGenerator._APP_PARAMETER_NAME,
                    router=AST.Expression(
                        AST.FunctionInvocation(
                            function_definition=AST.Reference(
                                qualified_name_excluding_import=(RegisterFileGenerator._REGISTER_SERVICE_FUNCTION_NAME,)
                            ),
                            args=[AST.Expression(service_initializer.get_parameter_name())],
                        )
                    ),
                )
            )
            writer.write_line()
        writer.write_line()
        writer.write_node(
            FastAPI.exception_handler(
                app_variable=RegisterFileGenerator._APP_PARAMETER_NAME,
                exception_type=self._context.core_utilities.FernHTTPException(),
                body=AST.CodeWriter(self._write_exception_handler_body),
            )
        )

    def _write_exception_handler_body(self, writer: AST.NodeWriter) -> None:
        writer.write(f"{FastAPI.EXCEPTION_HANDLER_REQUEST_ARGUMENT}.state.logger.info(")
        writer.write(f'f"{{{FastAPI.EXCEPTION_HANDLER_EXCEPTION_ARGUMENT}.__class__.__name__}} in ')
        writer.write(f'{{{FastAPI.EXCEPTION_HANDLER_REQUEST_ARGUMENT}.url.path}}", ')
        writer.write_line(f"exc_info={FastAPI.EXCEPTION_HANDLER_EXCEPTION_ARGUMENT})")

        writer.write_line(f"return {FastAPI.EXCEPTION_HANDLER_EXCEPTION_ARGUMENT}.to_json_response()")

    def _get_register_service_method(self) -> AST.FunctionDeclaration:
        return AST.FunctionDeclaration(
            name=RegisterFileGenerator._REGISTER_SERVICE_FUNCTION_NAME,
            signature=AST.FunctionSignature(
                parameters=[
                    AST.FunctionParameter(
                        name=RegisterFileGenerator._SERVICE_PARAMETER_NAME,
                        type_hint=AST.TypeHint(type=self._context.core_utilities.AbstractFernService()),
                    ),
                ],
                return_type=AST.TypeHint(type=FastAPI.APIRouter.REFERENCE),
            ),
            body=AST.CodeWriter(self._write_register_service_method_body),
        )

    def _write_register_service_method_body(self, writer: AST.NodeWriter) -> None:
        ROUTER_VARIABLE_NAME = "router"
        writer.write(f"{ROUTER_VARIABLE_NAME} = ")
        writer.write_node(FastAPI.APIRouter.invoke())
        writer.write_line()
        writer.write_line(
            f"type({RegisterFileGenerator._SERVICE_PARAMETER_NAME})."
            + f"{self._context.core_utilities.INIT_FERN_METHOD_NAME}"
            + f"({ROUTER_VARIABLE_NAME})",
        )
        writer.write_line(f"return {ROUTER_VARIABLE_NAME}")

    def _get_register_validators_method(self) -> AST.FunctionDeclaration:
        MODULE_PARAMETER = "module"

        def write_register_validators_method_body(writer: AST.NodeWriter) -> None:
            VALIDATORS_DIRECTORY_VARIABLE = "validators_directory"

            writer.write(f"{VALIDATORS_DIRECTORY_VARIABLE} = ")
            writer.write_node(
                AST.FunctionInvocation(
                    function_definition=AST.Reference(
                        import_=AST.ReferenceImport(module=AST.Module.built_in("os")),
                        qualified_name_excluding_import=("path", "dirname"),
                    ),
                    args=[AST.Expression(f"{MODULE_PARAMETER}.__file__")],
                )
            )
            writer.write_line()

            PATH_VARIABLE = "path"

            writer.write(f"for {PATH_VARIABLE} in ")
            writer.write_node(
                AST.FunctionInvocation(
                    function_definition=AST.Reference(
                        import_=AST.ReferenceImport(module=AST.Module.built_in("glob")),
                        qualified_name_excluding_import=("glob",),
                    ),
                    args=[AST.Expression('"**/*.py"')],
                    kwargs=[
                        ("root_dir", AST.Expression(VALIDATORS_DIRECTORY_VARIABLE)),
                        ("recursive", AST.Expression("True")),
                    ],
                )
            )
            writer.write_line(":")

            with writer.indent():
                ABSOLUTE_PATH_VARIABLE = "absolute_path"

                writer.write(f"{ABSOLUTE_PATH_VARIABLE} = ")
                writer.write_node(
                    AST.FunctionInvocation(
                        function_definition=AST.Reference(
                            import_=AST.ReferenceImport(module=AST.Module.built_in("os")),
                            qualified_name_excluding_import=("path", "join"),
                        ),
                        args=[AST.Expression(VALIDATORS_DIRECTORY_VARIABLE), AST.Expression(PATH_VARIABLE)],
                    )
                )
                writer.write_line()

                writer.write("if ")
                writer.write_node(
                    AST.FunctionInvocation(
                        function_definition=AST.Reference(
                            import_=AST.ReferenceImport(module=AST.Module.built_in("os")),
                            qualified_name_excluding_import=("path", "isfile"),
                        ),
                        args=[AST.Expression(ABSOLUTE_PATH_VARIABLE)],
                    )
                )
                writer.write_line(":")

                with writer.indent():
                    MODULE_PATH_VARIABLE = "module_path"

                    writer.write(f'{MODULE_PATH_VARIABLE} = ".".join(')
                    writer.write(f"[{MODULE_PARAMETER}.__name__] + ")
                    writer.write_line(f'{PATH_VARIABLE}.removesuffix(".py").split("/"))')

                    writer.write_node(
                        AST.FunctionInvocation(
                            function_definition=AST.Reference(
                                import_=AST.ReferenceImport(module=AST.Module.built_in("importlib")),
                                qualified_name_excluding_import=("import_module",),
                            ),
                            args=[AST.Expression(MODULE_PATH_VARIABLE)],
                        )
                    )
                    writer.write_line()

        return AST.FunctionDeclaration(
            name="register_validators",
            signature=AST.FunctionSignature(
                parameters=[
                    AST.FunctionParameter(
                        name=MODULE_PARAMETER,
                        type_hint=AST.TypeHint(
                            type=AST.ClassReference(
                                import_=AST.ReferenceImport(module=AST.Module.built_in("types")),
                                qualified_name_excluding_import=("ModuleType",),
                            )
                        ),
                    )
                ],
                return_type=AST.TypeHint.none(),
            ),
            body=AST.CodeWriter(code_writer=write_register_validators_method_body),
        )