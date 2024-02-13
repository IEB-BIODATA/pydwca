from dwca.utils import CamelCaseEnum


class LengthUnit(CamelCaseEnum):
    """
    The list of units which are of length type, or have a parentSI of meter SI.

    Attributes
    ----------
    METER : float
        International meter.
    NANOMETER : float
        International nanometer.
    MICROMETER : float
        International micrometer.
    MICRON : float
        Non International System of Units (SI) name of micrometer.
    MILLIMETER : float
        International millimeter.
    CENTIMETER : float
        International centimeter.
    DECIMETER : float
        International decimeter.
    DEKAMETER : float
        International dekameter.
    HECTOMETER : float
        International hectometer.
    KILOMETER : float
        International kilometer.
    MEGAMETER : float
        International megameter.
    ANGSTROM : float
        Ångström metric unit.
    INCH : float
         British imperial and United States customary inch.
    FOOT_US : float
        United States foot.
    FOOT : float
        International foot.
    FOOT_GOLD_COAST : float
        Gold Coast foot.
    FATHOM : float
        A measure (especially of depth) of six feet.
    NAUTICALMILE : float
        Nautical mile.
    YARD : float
        International yard.
    YARD_INDIAN : float
        Indian yard.
    LINK_CLARKE : float
        Link (Clarke's ratio).
    YARD_SEARS : float
        Yard (Sears).
    MILE : float
        International mile.
    """
    METER = 1e0
    NANOMETER = 1e-9
    MICROMETER = 1e-6
    MICRON = MICROMETER
    MILLIMETER = 1e-3
    CENTIMETER = 1e-2
    DECIMETER = 1e-1
    DEKAMETER = 1e1
    HECTOMETER = 1e2
    KILOMETER = 1e3
    MEGAMETER = 1e6
    ANGSTROM = 1e-10
    INCH = 0.0254
    FOOT_US = 0.3048006096012192
    FOOT = 0.3048
    FOOT_GOLD_COAST = 0.30479971018150881758
    FATHOM = 1.8288
    NAUTICALMILE = 1852
    YARD = 0.9144
    YARD_INDIAN = 0.9143985307444408
    LINK_CLARKE = 0.2011661949
    YARD_SEARS = 0.9143984146160287
    MILE = 1609.347218694438

    @property
    def valid_name(self) -> str:
        """
        Generate the valid name of the unit.

        Returns
        -------
        str
            Name of the unit.
        """
        return super().to_camel_case().capitalize()
