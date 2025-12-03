from typing import Literal, TypedDict
from collections.abc import Callable

Alert = Literal["alert"]
Article = Literal["article"]
Banner = Literal["banner"]
Button = Literal["button"]
Body = Literal["generic"]
Cell = Literal["cell"]
Checkbox = Literal["checkbox"]
ColumnHeader = Literal["columnheader"]
ComboBox = Literal["combobox"]
Complementary = Literal["complementary"]
ContentInfo = Literal["contentinfo"]
Definition = Literal["definition"]
Dialog = Literal["dialog"]
Figure = Literal["figure"]
Form = Literal["form"]
Generic = Literal["generic"]
Grid = Literal["grid"]
GridCell = Literal["gridcell"]
Group = Literal["group"]
Heading = Literal["heading"]
Html = Literal["document"]
Img = Literal["img"]
Image = Literal["image"]
Link = Literal["link"]
List = Literal["list"]
ListBox = Literal["listbox"]
ListItem = Literal["listitem"]
Main = Literal["main"]
Menu = Literal["menu"]
Meter = Literal["meter"]
Navigation = Literal["navigation"]
Option = Literal["option"]
Paragraph = Literal["paragraph"]
Presentation = Literal["presentation"]
ProgressBar = Literal["progressbar"]
Radio = Literal["radio"]
Region = Literal["region"]
Row = Literal["row"]
RowGroup = Literal["rowgroup"]
SearchBox = Literal["searchbox"]
Separator = Literal["separator"]
Status = Literal["status"]
Table = Literal["table"]
Term = Literal["term"]
TextBox = Literal["textbox"]
Time = Literal["time"]
TreeGrid = Literal["treegrid"]


AriaRoles = Literal[
    Alert,
    Article,
    Banner,
    Button,
    Body,
    Cell,
    Checkbox,
    ColumnHeader,
    ComboBox,
    Complementary,
    ContentInfo,
    Definition,
    Dialog,
    Figure,
    Form,
    Generic,
    Grid,
    GridCell,
    Group,
    Heading,
    Html,
    Img,
    Image,
    Link,
    List,
    ListBox,
    ListItem,
    Main,
    Menu,
    Meter,
    Navigation,
    Option,
    Paragraph,
    Presentation,
    ProgressBar,
    Radio,
    Region,
    Row,
    RowGroup,
    SearchBox,
    Separator,
    Status,
    Table,
    Term,
    TextBox,
    Time,
    TreeGrid,
]


class InputType(TypedDict):
    checkbox: Checkbox
    radio: Radio
    text: TextBox
    search: SearchBox
    button: Button
    password: TextBox


class ImplicitRoleMapping(TypedDict, total=False):
    a: Callable[[], str]
    article: Article
    address: Group
    aside: Complementary
    b: Generic
    button: Button
    body: Generic
    datalist: ListBox
    dd: Definition
    details: Group
    dialog: Dialog
    dl: List
    dt: Term
    fieldset: Group
    figure: Figure
    form: Form
    footer: Callable[[], str]
    header: Banner
    h1: Heading
    h2: Heading
    h3: Heading
    h4: Heading
    h5: Heading
    h6: Heading
    hr: Separator
    html: Html
    img: Callable[[], str]
    input: InputType
    li: ListItem
    main: Main
    menu: Menu
    meter: Meter
    nav: Navigation
    ol: List
    optgroup: Group
    option: Option
    output: Status
    p: Paragraph
    progress: ProgressBar
    section: Region
    select: Callable[[], str]
    summary: Button
    table: Table
    tbody: RowGroup
    td: Callable[[], str]
    textarea: TextBox
    tfoot: RowGroup
    th: ColumnHeader
    thead: RowGroup
    time: Time
    tr: Row
    ul: List
